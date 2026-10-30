import hmac
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Literal

from fastapi import APIRouter, Depends, Header, Query
from fastapi.responses import JSONResponse
from sqlalchemy import String, cast, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..deps import authed_user, require_role
from ..errors import ApiError
from ..idempotency import begin, save, validate_key
from ..models import Loan, User
from ..schemas import BorrowerCreate, BorrowerOut, BorrowerUpdate, Page
from ..security import hash_password
from .books import _like, pagination

router = APIRouter()
NOT_FOUND = ("NOT_FOUND", "Not found or unavailable.")


def _respond(user: User, status: int = 200, extra: dict | None = None) -> JSONResponse:
    payload = BorrowerOut.model_validate(user).model_dump(mode="json")
    headers = {"ETag": f'"{user.version}"', **(extra or {})}
    return JSONResponse(status_code=status, content=payload, headers=headers)


def _load(db: Session, borrower_id: uuid.UUID, lock: bool = False) -> User:
    stmt = select(User).where(User.id == borrower_id, User.role == "Borrower")
    if lock:
        stmt = stmt.with_for_update()  # version compare + update are atomic (API02)
    user = db.scalar(stmt)
    if user is None:
        raise ApiError(404, *NOT_FOUND)
    return user


def _parse_if_match(raw: str | None) -> int:
    if raw is None:
        raise ApiError(428, "PRECONDITION_REQUIRED", "If-Match header is required.")
    m = re.fullmatch(r'"(\d+)"', raw.strip())
    if not m:
        raise ApiError(422, "VALIDATION_ERROR", "Some fields are invalid.",
                       {"If-Match": "Must be a quoted version number, for example \"3\"."})
    return int(m.group(1))


def _check_version(user: User, expected: int) -> None:
    if user.version != expected:
        raise ApiError(412, "VERSION_CONFLICT", "This profile has changed. Refresh it before saving.")


def _check_password(password: str, email: str) -> None:
    if password.lower() == email:
        raise ApiError(422, "VALIDATION_ERROR", "Some fields are invalid.",
                       {"temporary_password": "Password must differ from the e-mail."})


def _email_taken(db: Session, email: str, exclude: uuid.UUID | None = None) -> bool:
    stmt = select(User.id).where(User.email == email)
    if exclude:
        stmt = stmt.where(User.id != exclude)
    return db.scalar(stmt) is not None


def _duplicate_email():
    return ApiError(409, "DUPLICATE_EMAIL", "A user with this e-mail already exists.")


# ---------- Create (FR01, FR02) ----------

@router.post("/borrowers", status_code=201, response_model=BorrowerOut)
def create_borrower(
    body: BorrowerCreate,
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
    librarian: User = Depends(require_role("Librarian")),
    db: Session = Depends(get_db),
):
    key = validate_key(idempotency_key)
    operation = "POST /borrowers"

    # Never store a plain hash of the password: keep a keyed digest in the request hash
    fingerprint = body.model_dump(mode="json")
    fingerprint["temporary_password"] = hmac.new(
        settings.secret_key.encode(), body.temporary_password.encode(), "sha256").hexdigest()
    digest, replay = begin(db, librarian, operation, key, fingerprint)
    if replay:
        data = json.loads(replay.body)
        replay.headers["ETag"] = f'"{data["version"]}"'
        replay.headers["Location"] = f'/api/v1/borrowers/{data["id"]}'
        return replay

    _check_password(body.temporary_password, body.email)
    if _email_taken(db, body.email):
        raise _duplicate_email()

    user = User(
        full_name=body.full_name, email=body.email, role="Borrower",
        phone=body.phone, address=body.address,
        password_hash=hash_password(body.temporary_password),
        must_change_password=True,
    )
    db.add(user)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise _duplicate_email()
    db.refresh(user)

    payload = BorrowerOut.model_validate(user).model_dump(mode="json")
    save(db, librarian, operation, key, digest, 201, payload)
    db.commit()
    return _respond(user, 201, {"Location": f"/api/v1/borrowers/{user.id}"})


# ---------- List and read (U02, U03, FR03) ----------

@router.get("/borrowers", response_model=Page[BorrowerOut])
def list_borrowers(
    q: str | None = Query(None, max_length=100),
    status: Literal["active", "removed"] | None = None,
    paging: tuple = Depends(pagination),
    _: User = Depends(require_role("Librarian")),
    db: Session = Depends(get_db),
):
    page, page_size = paging
    conds = [User.role == "Borrower"]
    q = (q or "").strip()
    if q:
        pattern = _like(q)
        member_no = func.concat("MB-", func.lpad(cast(User.member_seq, String), 6, "0"))
        conds.append(or_(
            User.full_name.ilike(pattern, escape="\\"),
            User.email.ilike(pattern, escape="\\"),
            member_no.ilike(pattern, escape="\\"),
        ))
    if status:
        conds.append(User.status == status.capitalize())

    total = db.scalar(select(func.count()).select_from(User).where(*conds))
    rows = db.scalars(
        select(User).where(*conds).order_by(User.full_name, User.id)
        .offset((page - 1) * page_size).limit(page_size)
    ).all()
    return {"items": rows, "page": page, "page_size": page_size, "total": total}


@router.get("/borrowers/{borrower_id}", response_model=BorrowerOut)
def get_borrower(borrower_id: uuid.UUID, user: User = Depends(authed_user),
                 db: Session = Depends(get_db)):
    # A borrower may read only their own profile; anything else looks nonexistent (P03)
    if user.role == "Borrower" and user.id != borrower_id:
        raise ApiError(404, *NOT_FOUND)
    return _respond(_load(db, borrower_id))


# ---------- Edit (FR05, P11) ----------

@router.patch("/borrowers/{borrower_id}", response_model=BorrowerOut)
def edit_borrower(
    borrower_id: uuid.UUID,
    body: BorrowerUpdate,
    if_match: str | None = Header(default=None, alias="If-Match"),
    _: User = Depends(require_role("Librarian")),
    db: Session = Depends(get_db),
):
    supplied = body.model_fields_set
    if not supplied:
        raise ApiError(422, "VALIDATION_ERROR", "Some fields are invalid.",
                       {"request": "Supply at least one field to change."})

    borrower = _load(db, borrower_id, lock=True)
    expected = _parse_if_match(if_match)
    if borrower.status == "Removed":
        raise ApiError(409, "PROFILE_REMOVED", "This profile has been removed.")
    _check_version(borrower, expected)

    changed = False
    if "full_name" in supplied and body.full_name != borrower.full_name:
        borrower.full_name, changed = body.full_name, True
    if "email" in supplied and body.email != borrower.email:
        if _email_taken(db, body.email, exclude=borrower.id):
            raise _duplicate_email()
        borrower.email, changed = body.email, True
    if "phone" in supplied and body.phone != borrower.phone:
        borrower.phone, changed = body.phone, True
    if "address" in supplied and body.address != borrower.address:
        borrower.address, changed = body.address, True
    if "temporary_password" in supplied:
        _check_password(body.temporary_password, borrower.email)
        borrower.password_hash = hash_password(body.temporary_password)
        borrower.must_change_password = True
        borrower.failed_login_count = 0
        borrower.locked_until = None
        changed = True

    if not changed:  # no-op: no version bump, nothing written (P11)
        return _respond(borrower)

    borrower.version += 1
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise _duplicate_email()
    db.refresh(borrower)
    return _respond(borrower)


# ---------- Remove (FR06, P10) ----------

@router.delete("/borrowers/{borrower_id}", response_model=BorrowerOut)
def remove_borrower(
    borrower_id: uuid.UUID,
    if_match: str | None = Header(default=None, alias="If-Match"),
    _: User = Depends(require_role("Librarian")),
    db: Session = Depends(get_db),
):
    borrower = _load(db, borrower_id, lock=True)
    expected = _parse_if_match(if_match)
    if borrower.status == "Removed":
        raise ApiError(409, "PROFILE_REMOVED", "This profile has already been removed.")
    _check_version(borrower, expected)

    active = db.scalar(select(func.count()).select_from(Loan)
                       .where(Loan.borrower_id == borrower.id, Loan.status == "Borrowed"))
    if active:
        raise ApiError(409, "HAS_ACTIVE_LOANS", "This borrower still has books on loan.")

    # Soft removal: history stays, sign-in stops, e-mail stays reserved
    borrower.status = "Removed"
    borrower.removed_at = datetime.now(timezone.utc)
    borrower.version += 1
    db.commit()
    db.refresh(borrower)
    return _respond(borrower)