import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone

from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from .errors import ApiError
from .models import IdempotencyRecord, User

RETENTION = timedelta(hours=24)


def validate_key(raw: str | None) -> str:
    try:
        return str(uuid.UUID(raw or ""))
    except ValueError:
        raise ApiError(422, "VALIDATION_ERROR", "Some fields are invalid.",
                       {"Idempotency-Key": "A UUID Idempotency-Key header is required."})


def begin(db: Session, user: User, operation: str, key: str, body: dict):
    """Returns (request_hash, replay_response_or_None)."""
    digest = hashlib.sha256(json.dumps(body, sort_keys=True, default=str).encode()).hexdigest()
    # Serializes simultaneous requests with the same key until this transaction ends
    db.execute(text("SELECT pg_advisory_xact_lock(hashtext(:k))"),
               {"k": f"{user.id}:{operation}:{key}"})

    record = db.get(IdempotencyRecord, (user.id, operation, key))
    if record and record.expires_at <= datetime.now(timezone.utc):
        db.delete(record)
        db.flush()
        record = None

    if record:
        if record.request_hash != digest:
            raise ApiError(409, "IDEMPOTENCY_CONFLICT",
                           "This key was already used with a different request.")
        return digest, JSONResponse(status_code=record.response_status, content=record.response_body)
    return digest, None


def save(db: Session, user: User, operation: str, key: str, digest: str, status: int, body: dict):
    db.add(IdempotencyRecord(
        user_id=user.id, operation=operation, key=key, request_hash=digest,
        response_status=status, response_body=body,
        expires_at=datetime.now(timezone.utc) + RETENTION,
    ))