from fastapi import Depends, Request
from sqlalchemy.orm import Session

from .database import get_db
from .errors import ApiError
from .models import User
from .security import SESSION_COOKIE, decode_token, role_for_email


def current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Authenticated, active account (P01). Allowed even if a password change is pending."""
    token = request.cookies.get(SESSION_COOKIE)
    user_id = decode_token(token) if token else None
    user = db.get(User, user_id) if user_id else None
    if (
        user is None
        or user.status != "Active"                      # removed users are rejected (P04)
        or role_for_email(user.email) != user.role      # domain and role must match (P02)
    ):
        raise ApiError(401, "UNAUTHENTICATED", "Please sign in.")
    return user


def authed_user(user: User = Depends(current_user)) -> User:
    if user.must_change_password:
        raise ApiError(403, "PASSWORD_CHANGE_REQUIRED", "You must change your password first.")
    return user


def require_role(*roles: str):
    def dependency(user: User = Depends(authed_user)) -> User:
        if user.role not in roles:
            raise ApiError(403, "FORBIDDEN", "This action is unavailable for your account.")
        return user
    return dependency