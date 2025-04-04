from fastapi.responses import JSONResponse
from typing import Any, Optional

def success_response(message: str, data: Optional[Any] = None, status_code: int = 200, headers: Optional[dict] = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "statusCode": status_code,
            "data": data
        },
        headers=headers
    )

def error_response(message: str, status_code: int = 500, errors: Optional[Any] = None):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "statusCode": status_code,
            "errors": errors
        }
    )
