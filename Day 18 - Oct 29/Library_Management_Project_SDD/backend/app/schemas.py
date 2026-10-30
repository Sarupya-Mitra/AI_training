import re
import uuid
from datetime import datetime, timezone
from typing import Annotated, Generic, TypeVar

from pydantic import (
    BaseModel, ConfigDict, Field, StringConstraints, computed_field, field_validator,
)

T = TypeVar("T")

Title = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]
Author = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=150)]
Category = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=60)]


class Page(BaseModel, Generic[T]):
    items: list[T]
    page: int
    page_size: int
    total: int


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str
    role: str
    full_name: str
    member_number: str | None = None
    must_change_password: bool


class BookCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")  # unknown fields are rejected (spec Section 8)

    isbn: str
    title: Title
    author: Author
    publisher: str | None = Field(default=None, max_length=150)
    category: Category
    publication_year: int = Field(ge=1000)
    total_copies: int = Field(ge=1, le=1000)

    @field_validator("isbn")
    @classmethod
    def clean_isbn(cls, v: str) -> str:
        digits = re.sub(r"[\s-]", "", v)
        if not digits.isdigit() or len(digits) not in (10, 13):
            raise ValueError("ISBN must have 10 or 13 digits.")
        return digits

    @field_validator("publisher", mode="before")
    @classmethod
    def blank_publisher(cls, v):
        if isinstance(v, str):
            v = v.strip()
        return v or None

    @field_validator("publication_year")
    @classmethod
    def not_in_future(cls, v: int) -> int:
        if v > datetime.now(timezone.utc).year:
            raise ValueError("Publication year cannot be in the future.")
        return v


class BookPublic(BaseModel):
    """What visitors and borrowers may see. No total_copies (FR08)."""
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    isbn: str
    title: str
    author: str
    publisher: str | None
    category: str
    publication_year: int
    available_copies: int


class BookInventory(BookPublic):
    """Librarian view (FR09)."""
    book_code: str
    total_copies: int
    created_at: datetime

    @computed_field
    @property
    def on_loan(self) -> int:
        return self.total_copies - self.available_copies


class EventOut(BaseModel):
    id: uuid.UUID
    event_type: str
    quantity_delta: int
    available_after: int
    loan_id: uuid.UUID | None
    actor_id: uuid.UUID
    actor_name: str
    occurred_at: datetime

# ---------- Borrower profiles ----------

_EMAIL_RE = re.compile(r"^[a-z0-9._%+\-]+@bor\.sample\.com$")
_PHONE_RE = re.compile(r"^\+?\d{7,15}$")

FullName = Annotated[str, StringConstraints(strip_whitespace=True, min_length=2, max_length=100)]
Password = Annotated[str, StringConstraints(min_length=12, max_length=128)]


def _check_email(v: str) -> str:
    v = v.strip().lower()
    if len(v) > 254 or not _EMAIL_RE.match(v):
        raise ValueError("E-mail must be a valid @bor.sample.com address.")
    return v


def _check_phone(v: str | None) -> str | None:
    if v is None:
        return None
    v = v.strip()
    if not v:
        return None
    if not _PHONE_RE.match(v):
        raise ValueError("Phone must be 7-15 digits with an optional leading +.")
    return v


def _check_address(v: str | None) -> str | None:
    if v is None:
        return None
    v = v.strip()
    if len(v) > 300:
        raise ValueError("Address must be at most 300 characters.")
    return v or None


class BorrowerCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    full_name: FullName
    email: str
    phone: str | None = None
    address: str | None = None
    temporary_password: Password

    _email = field_validator("email")(lambda cls, v: _check_email(v))
    _phone = field_validator("phone")(lambda cls, v: _check_phone(v))
    _address = field_validator("address")(lambda cls, v: _check_address(v))


class BorrowerUpdate(BaseModel):
    """Partial update. Only supplied fields change (FR05)."""
    model_config = ConfigDict(extra="forbid")

    full_name: FullName | None = None
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    temporary_password: Password | None = None

    @field_validator("full_name", "email", "temporary_password")
    @classmethod
    def not_null(cls, v):
        if v is None:
            raise ValueError("This field cannot be null.")
        return v

    @field_validator("email")
    @classmethod
    def email_rule(cls, v):
        return _check_email(v)

    _phone = field_validator("phone")(lambda cls, v: _check_phone(v))
    _address = field_validator("address")(lambda cls, v: _check_address(v))


class BorrowerOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    member_number: str | None
    full_name: str
    email: str
    phone: str | None
    address: str | None
    status: str
    must_change_password: bool
    created_at: datetime
    updated_at: datetime
    removed_at: datetime | None
    version: int