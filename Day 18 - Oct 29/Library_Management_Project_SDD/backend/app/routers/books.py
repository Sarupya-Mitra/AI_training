import uuid

from fastapi import APIRouter, Depends, Header, Query
from fastapi.responses import JSONResponse
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database import get_db
from ..deps import require_role
from ..errors import ApiError
from ..idempotency import begin, save, validate_key
from ..models import Book, InventoryEvent, User
from ..schemas import BookCreate, BookInventory, BookPublic, EventOut, Page

router = APIRouter()


def pagination(page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100)):
    return page, page_size


def _like(q: str) -> str:
    """Literal substring match: escape LIKE wildcards (API01)."""
    escaped = q.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    return f"%{escaped}%"


def _conditions(q: str | None, category: str | None) -> list:
    conds = []
    q = (q or "").strip()
    if q:
        pattern = _like(q)
        conds.append(or_(
            Book.title.ilike(pattern, escape="\\"),
            Book.author.ilike(pattern, escape="\\"),
            Book.isbn.ilike(pattern, escape="\\"),
        ))
    if category and category.strip():
        conds.append(func.lower(Book.category) == category.strip().lower())
    return conds


def _paged(db: Session, conds: list, page: int, page_size: int) -> dict:
    total = db.scalar(select(func.count()).select_from(Book).where(*conds))
    rows = db.scalars(
        select(Book).where(*conds)
        .order_by(Book.title, Book.id)          # title ascending, then id (API01)
        .offset((page - 1) * page_size).limit(page_size)
    ).all()
    return {"items": rows, "page": page, "page_size": page_size, "total": total}


# ---------- Public (U09) ----------

@router.get("/books", response_model=Page[BookPublic])
def list_books(
    q: str | None = Query(None, max_length=100),
    category: str | None = Query(None, max_length=60),
    available: bool = False,
    paging: tuple = Depends(pagination),
    db: Session = Depends(get_db),
):
    conds = _conditions(q, category)
    if available:
        conds.append(Book.available_copies > 0)
    return _paged(db, conds, *paging)


@router.get("/books/{book_id}", response_model=BookPublic)
def get_book(book_id: uuid.UUID, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    if book is None:
        raise ApiError(404, "NOT_FOUND", "Not found or unavailable.")
    return book


# ---------- Librarian only (U05, U06) ----------

@router.post("/books", status_code=201, response_model=BookInventory)
def add_book(
    body: BookCreate,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    user: User = Depends(require_role("Librarian")),
    db: Session = Depends(get_db),
):
    key = validate_key(idempotency_key)
    operation = "POST /books"
    digest, replay = begin(db, user, operation, key, body.model_dump(mode="json"))
    if replay:
        return replay

    if db.scalar(select(Book.id).where(Book.isbn == body.isbn)):
        raise ApiError(409, "DUPLICATE_ISBN", "A book with this ISBN already exists.")

    book = Book(**body.model_dump(), available_copies=body.total_copies, created_by=user.id)
    db.add(book)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise ApiError(409, "DUPLICATE_ISBN", "A book with this ISBN already exists.")
    db.refresh(book)

    # FR14: every change to available copies has exactly one event
    db.add(InventoryEvent(
        book_id=book.id, event_type="Added", quantity_delta=body.total_copies,
        available_after=body.total_copies, actor_id=user.id,
    ))
    payload = BookInventory.model_validate(book).model_dump(mode="json")
    save(db, user, operation, key, digest, 201, payload)
    db.commit()  # book, event and idempotency record commit together

    return JSONResponse(status_code=201, content=payload,
                        headers={"Location": f"/api/v1/books/{book.id}"})


@router.get("/inventory", response_model=Page[BookInventory])
def inventory(
    q: str | None = Query(None, max_length=100),
    category: str | None = Query(None, max_length=60),
    out_of_stock: bool = False,
    paging: tuple = Depends(pagination),
    _: User = Depends(require_role("Librarian")),
    db: Session = Depends(get_db),
):
    conds = _conditions(q, category)
    if out_of_stock:
        conds.append(Book.available_copies == 0)
    return _paged(db, conds, *paging)


@router.get("/inventory/{book_id}/events", response_model=Page[EventOut])
def inventory_events(
    book_id: uuid.UUID,
    paging: tuple = Depends(pagination),
    _: User = Depends(require_role("Librarian")),
    db: Session = Depends(get_db),
):
    if db.get(Book, book_id) is None:
        raise ApiError(404, "NOT_FOUND", "Not found or unavailable.")
    page, page_size = paging
    total = db.scalar(select(func.count()).select_from(InventoryEvent)
                      .where(InventoryEvent.book_id == book_id))
    rows = db.execute(
        select(InventoryEvent, User.full_name)
        .join(User, User.id == InventoryEvent.actor_id)
        .where(InventoryEvent.book_id == book_id)
        .order_by(InventoryEvent.occurred_at, InventoryEvent.id)   # oldest first
        .offset((page - 1) * page_size).limit(page_size)
    ).all()
    items = [
        EventOut(id=e.id, event_type=e.event_type, quantity_delta=e.quantity_delta,
                 available_after=e.available_after, loan_id=e.loan_id,
                 actor_id=e.actor_id, actor_name=name, occurred_at=e.occurred_at)
        for e, name in rows
    ]
    return {"items": items, "page": page, "page_size": page_size, "total": total}