from fastapi.exceptions import (
    HTTPException,
    RequestValidationError,
    ResponseValidationError,
)
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from tortoise.exceptions import DoesNotExist, IntegrityError
from fastapi import HTTPException, status


class SettingNotFound(Exception):
    pass

async def DoesNotExistHandle(req: Request, exc: DoesNotExist) -> JSONResponse:
    content = dict(
        code=404,
        msg=f"Object has not found, exc: {exc}, query_params: {req.query_params}",
    )
    return JSONResponse(content=content, status_code=404)


async def IntegrityHandle(_: Request, exc: IntegrityError) -> JSONResponse:
    content = dict(
        code=500,
        msg=f"IntegrityError，{exc}",
    )
    return JSONResponse(content=content, status_code=500)


async def HttpExcHandle(_: Request, exc: HTTPException) -> JSONResponse:
    content = dict(code=exc.status_code, msg=exc.detail, data=None)
    return JSONResponse(content=content, status_code=exc.status_code)


async def RequestValidationHandle(_: Request, exc: RequestValidationError) -> JSONResponse:
    content = dict(code=422, msg=f"RequestValidationError, {exc}")
    return JSONResponse(content=content, status_code=422)


async def ResponseValidationHandle(_: Request, exc: ResponseValidationError) -> JSONResponse:
    content = dict(code=500, msg=f"ResponseValidationError, {exc}")
    return JSONResponse(content=content, status_code=500)

def raise_field_error(field: str, message: str):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail={
            "code": 400,
            "msg": "Validation Error",
            "data": {
                field: [message]
            }
        }
    )

# async def raise_field_error(field: str, message: str):
#     content = dict(code=status.HTTP_400_BAD_REQUEST, msg=None, data={
#                 field: [message]
#             })
#     return JSONResponse(content=content, status_code=400)

