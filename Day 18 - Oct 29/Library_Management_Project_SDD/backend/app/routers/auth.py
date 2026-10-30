from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Response
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..deps import current_user
from ..errors import ApiError
from ..models import User
from ..schemas import UserOut
from ..security import (
    SESSION_COOKIE, create_token, hash_password, role_for_email, verify_password,
)

router = APIRouter()

MAX_FAILED = 5
LOCK_MINUTES = 15


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: str = Field(max_length=254)
    password: str = Field(max_length=128)


class ChangePasswordRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    current_password: str = Field(max_length=128)
    new_password: str = Field(min_length=12, max_length=128)


@router.post("/auth/login", response_model=UserOut)
def login(body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    email = body.email.strip().lower()
    now = datetime.now(timezone.utc)
    user = db.scalar(select(User).where(User.email == email))

    if user and user.locked_until and user.locked_until > now:
        raise ApiError(429, "TOO_MANY_REQUESTS", "Too many failed attempts. Try again later.")

    ok = (
        user is not None
        and user.status == "Active"
        and role_for_email(user.email) == user.role
        and verify_password(user.password_hash, body.password)
    )
    if not ok:
        if user:
            user.failed_login_count += 1
            if user.failed_login_count >= MAX_FAILED:
                user.locked_until = now + timedelta(minutes=LOCK_MINUTES)
                user.failed_login_count = 0
            db.commit()  # commit before raising so the counter is kept
        # Same generic answer for every failure (P02)
        raise ApiError(401, "INVALID_CREDENTIALS", "Invalid e-mail or password.")

    user.failed_login_count = 0
    user.locked_until = None
    db.commit()

    response.set_cookie(
        SESSION_COOKIE,
        create_token(user.id),
        max_age=settings.access_token_minutes * 60,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        path="/",
    )
    return user


@router.post("/auth/logout", status_code=204)
def logout(response: Response):
    response.delete_cookie(SESSION_COOKIE, path="/")
    response.status_code = 204
    return response


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user


@router.post("/auth/change-password", status_code=204)
def change_password(body: ChangePasswordRequest, user: User = Depends(current_user),
                    db: Session = Depends(get_db)):
    if not verify_password(user.password_hash, body.current_password):
        raise ApiError(422, "VALIDATION_ERROR", "Some fields are invalid.",
                       {"current_password": "Current password is incorrect."})
    if body.new_password.lower() == user.email:
        raise ApiError(422, "VALIDATION_ERROR", "Some fields are invalid.",
                       {"new_password": "Password must differ from your e-mail."})
    if body.new_password == body.current_password:
        raise ApiError(422, "VALIDATION_ERROR", "Some fields are invalid.",
                       {"new_password": "New password must differ from the current one."})
    user.password_hash = hash_password(body.new_password)
    user.must_change_password = False
    db.commit()
    return Response(status_code=204)