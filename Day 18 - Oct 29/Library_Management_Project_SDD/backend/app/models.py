import uuid
from datetime import date, datetime

from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, Date, DateTime, ForeignKey,
    Identity, Index, Integer, String, Uuid, func, text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .database import Base


class User(Base):
    """Account + borrower profile."""
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    # Identity column: never reused, gaps allowed. member number = MB-000001 etc.
    member_seq: Mapped[int] = mapped_column(BigInteger, Identity(start=1), unique=True)
    full_name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(254), unique=True)  # stored lowercase
    role: Mapped[str] = mapped_column(String(20))
    phone: Mapped[str | None] = mapped_column(String(20))
    address: Mapped[str | None] = mapped_column(String(300))
    status: Mapped[str] = mapped_column(String(10), default="Active", server_default="Active")
    password_hash: Mapped[str] = mapped_column(String(255))
    must_change_password: Mapped[bool] = mapped_column(Boolean, default=True, server_default=text("true"))
    failed_login_count: Mapped[int] = mapped_column(Integer, default=0, server_default="0")
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    removed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    version: Mapped[int] = mapped_column(Integer, default=1, server_default="1")

    __table_args__ = (
        CheckConstraint("role IN ('Librarian','Borrower')", name="ck_users_role"),
        CheckConstraint("status IN ('Active','Removed')", name="ck_users_status"),
        CheckConstraint("email = lower(email)", name="ck_users_email_lower"),
        # Spec P02: role must match the e-mail domain
        CheckConstraint(
            "(role = 'Librarian' AND right(email, 15) = '@lib.sample.com') OR "
            "(role = 'Borrower' AND right(email, 15) = '@bor.sample.com')",
            name="ck_users_email_domain",
        ),
    )

    @property
    def member_number(self) -> str | None:
        return f"MB-{self.member_seq:06d}" if self.role == "Borrower" else None


class Book(Base):
    """Inventory record."""
    __tablename__ = "books"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    book_seq: Mapped[int] = mapped_column(BigInteger, Identity(start=1), unique=True)
    isbn: Mapped[str] = mapped_column(String(13), unique=True)
    title: Mapped[str] = mapped_column(String(200), index=True)
    author: Mapped[str] = mapped_column(String(150), index=True)
    publisher: Mapped[str | None] = mapped_column(String(150))
    category: Mapped[str] = mapped_column(String(60), index=True)
    publication_year: Mapped[int] = mapped_column(Integer)
    total_copies: Mapped[int] = mapped_column(Integer)
    available_copies: Mapped[int] = mapped_column(Integer)
    created_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("length(isbn) IN (10, 13)", name="ck_books_isbn_len"),
        CheckConstraint("total_copies BETWEEN 1 AND 1000", name="ck_books_total"),
        # Spec Section 6: 0 <= available_copies <= total_copies
        CheckConstraint("available_copies >= 0 AND available_copies <= total_copies", name="ck_books_available"),
    )

    @property
    def book_code(self) -> str:
        return f"BK-{self.book_seq:06d}"


class Loan(Base):
    __tablename__ = "loans"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    loan_seq: Mapped[int] = mapped_column(BigInteger, Identity(start=1), unique=True)
    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id"), index=True)
    borrower_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    borrowed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    due_date: Mapped[date] = mapped_column(Date, index=True)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    returned_by: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(10), default="Borrowed", server_default="Borrowed", index=True)

    __table_args__ = (
        CheckConstraint("status IN ('Borrowed','Returned')", name="ck_loans_status"),
        # A borrower can have only one active loan per book
        Index("uq_loans_active_borrower_book", "borrower_id", "book_id",
              unique=True, postgresql_where=text("status = 'Borrowed'")),
    )

    @property
    def loan_number(self) -> str:
        return f"LN-{self.loan_seq:06d}"


class InventoryEvent(Base):
    """Append-only log of every change to available copies."""
    __tablename__ = "inventory_events"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    book_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("books.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(10))
    quantity_delta: Mapped[int] = mapped_column(Integer)
    available_after: Mapped[int] = mapped_column(Integer)
    loan_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("loans.id"))
    actor_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    occurred_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        CheckConstraint("event_type IN ('Added','Borrowed','Returned')", name="ck_events_type"),
    )


class IdempotencyRecord(Base):
    __tablename__ = "idempotency_records"

    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), primary_key=True)
    operation: Mapped[str] = mapped_column(String(60), primary_key=True)
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    request_hash: Mapped[str] = mapped_column(String(64))
    response_status: Mapped[int] = mapped_column(Integer)
    response_body: Mapped[dict] = mapped_column(JSONB)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))