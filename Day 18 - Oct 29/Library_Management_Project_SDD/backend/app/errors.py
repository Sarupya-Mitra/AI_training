from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, fields: dict | None = None):
        self.status = status
        self.code = code
        self.message = message
        self.fields = fields or {}


def error_response(request: Request, status: int, code: str, message: str, fields: dict | None = None):
    return JSONResponse(
        status_code=status,
        content={"error": {
            "code": code,
            "message": message,
            "fields": fields or {},
            "request_id": getattr(request.state, "request_id", ""),
        }},
    )


_STATUS_CODES = {401: "UNAUTHENTICATED", 403: "FORBIDDEN", 404: "NOT_FOUND", 405: "METHOD_NOT_ALLOWED"}


def register_error_handlers(app: FastAPI) -> None:
    @app.exception_handler(ApiError)
    async def _api_error(request: Request, exc: ApiError):
        return error_response(request, exc.status, exc.code, exc.message, exc.fields)

    @app.exception_handler(RequestValidationError)
    async def _validation_error(request: Request, exc: RequestValidationError):
        errors = exc.errors()
        if any(e["type"] == "json_invalid" for e in errors):
            return error_response(request, 400, "MALFORMED_JSON", "Request cannot be parsed.")
        fields = {}
        for e in errors:
            name = ".".join(str(p) for p in e["loc"] if p not in ("body", "query", "path", "header", "cookie"))
            fields[name or "request"] = e["msg"]
        return error_response(request, 422, "VALIDATION_ERROR", "Some fields are invalid.", fields)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(request: Request, exc: StarletteHTTPException):
        code = _STATUS_CODES.get(exc.status_code, "ERROR")
        message = "Not found or unavailable." if exc.status_code == 404 else "Request could not be completed."
        return error_response(request, exc.status_code, code, message)

    @app.exception_handler(Exception)
    async def _unexpected(request: Request, exc: Exception):
        # No internal details are exposed (spec Section 8)
        return error_response(request, 500, "INTERNAL_ERROR", "Something went wrong.")