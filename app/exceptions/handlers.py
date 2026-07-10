"""
Global exception handlers.

Provides consistent error responses across the API.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse


async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    """
    Handle FastAPI HTTP exceptions.
    """

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "status_code": exc.status_code,
            "message": exc.detail,
        },
    )


async def unhandled_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Handle unexpected server errors.
    """

    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "status_code": 500,
            "message": "Internal server error.",
        },
    )


def register_exception_handlers(app: FastAPI):
    """
    Register all global exception handlers.
    """

    app.add_exception_handler(
        HTTPException,
        http_exception_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_exception_handler,
    )