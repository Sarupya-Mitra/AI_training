import uuid

from fastapi import APIRouter, Depends, FastAPI, Request
from sqlalchemy import text
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .errors import error_response, register_error_handlers
from .routers import auth,books,borrowers


app = FastAPI(title="Library Management API", version="1.0")
register_error_handlers(app)

SAFE_METHODS = {"GET", "HEAD", "OPTIONS"}


@app.middleware("http")
async def request_context(request: Request, call_next):
    request.state.request_id = str(uuid.uuid4())

    # CSRF guard (NF02): browser writes must come from an allowed origin
    origin = request.headers.get("origin")
    if request.method not in SAFE_METHODS and origin and origin not in settings.allowed_origins:
        return error_response(request, 403, "FORBIDDEN", "Origin not allowed.")

    response = await call_next(request)
    response.headers["X-Request-ID"] = request.state.request_id
    return response


api = APIRouter(prefix="/api/v1")


@api.get("/health")
def health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


api.include_router(auth.router)
api.include_router(books.router)
api.include_router(borrowers.router)
app.include_router(api)