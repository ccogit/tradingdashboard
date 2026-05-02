from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import Request


class AppException(Exception):
    def __init__(self, status_code: int, code: str, message: str):
        self.status_code = status_code
        self.code = code
        self.message = message


class IBNotConnectedError(AppException):
    def __init__(self):
        super().__init__(503, "IB_NOT_CONNECTED", "IB Gateway is not connected")


class IBOrderError(AppException):
    def __init__(self, message: str):
        super().__init__(422, "IB_ORDER_ERROR", message)


class ContractNotFound(AppException):
    def __init__(self, query: str):
        super().__init__(404, "CONTRACT_NOT_FOUND", f"No contract found for: {query}")


class InsufficientPermissions(AppException):
    def __init__(self):
        super().__init__(403, "INSUFFICIENT_PERMISSIONS", "You do not have access to this resource")


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"code": exc.code, "message": exc.message},
    )
