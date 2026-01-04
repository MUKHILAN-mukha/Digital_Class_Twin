from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError
import traceback


def register_error_handlers(app):
    """
    Global error handlers to prevent frontend crashes
    (Sheet-1 B10)
    """

    # ─────────────────────────────
    # HTTP EXCEPTIONS (401, 403, 404, etc.)
    # ─────────────────────────────
    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request,
        exc: StarletteHTTPException
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": exc.detail,
                "status_code": exc.status_code,
                "path": str(request.url)
            }
        )

    # ─────────────────────────────
    # VALIDATION ERRORS (422)
    # ─────────────────────────────
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        return JSONResponse(
            status_code=422,
            content={
                "error": "validation_error",
                "details": exc.errors()
            }
        )

    # ─────────────────────────────
    # DATABASE ERRORS
    # ─────────────────────────────
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(
        request: Request,
        exc: SQLAlchemyError
    ):
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": "database_error",
                "message": "Internal database error"
            }
        )

    # ─────────────────────────────
    # CATCH-ALL (500)
    # ─────────────────────────────
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception
    ):
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": "internal_server_error",
                "message": "Unexpected server error"
            }
        )
