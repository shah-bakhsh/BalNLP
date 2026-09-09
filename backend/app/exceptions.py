from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from balnlp.exceptions import BalNLPError


def error_response(code, message, status):
    return JSONResponse({"error": {"code": code, "message": message}}, status_code=status)


def register_handlers(app):
    @app.exception_handler(BalNLPError)
    async def domain_error(request, error):
        return error_response(error.code, error.message, error.status)

    @app.exception_handler(RequestValidationError)
    async def validation_error(request, error):
        fields = {part for item in error.errors() for part in item["loc"]}
        code = "INVALID_TASKS" if "tasks" in fields else "INVALID_TEXT"
        message = (
            "Choose supported tasks."
            if code == "INVALID_TASKS"
            else "Send a JSON object with a text string."
        )
        return error_response(code, message, 422)

    @app.exception_handler(HTTPException)
    async def http_error(request, error):
        return error_response(
            "HTTP_ERROR", "The requested operation is not available.", error.status_code
        )

    @app.exception_handler(Exception)
    async def unexpected_error(request, error):
        return error_response(
            "INTERNAL_ERROR",
            "The service encountered an unexpected error. Please try again later.",
            500,
        )
