from pydantic import BaseModel
from fastapi.responses import JSONResponse

class ErrorResponse(BaseModel):
    code: str
    message: str
    correlation_id: str

class CustomerNotFoundException(Exception):
    pass
class ComplaintNotFoundException(Exception):
    pass
class InvalidStatusTransitionException(Exception):
    pass

def create_error(status_code : int, code : str, message: str, correlation_id):
    return JSONResponse(status_code = status_code, content={
        "code": code,
        "message": message,
        "correlation_id": correlation_id
    })

async def customer_not_found(request, exc):
    return create_error(404, "CUSTOMER_NOT_FOUND", str(exc), request.state.correlation_id)

async def complaint_not_found(request, exc):
    return create_error(404, "COMPLAINT_NOT_FOUND", str(exc), request.state.correlation_id)

async def invalid_status_transition(request, exc):
    return create_error(409, "INVALID_STATUS_TRANSITION", str(exc), request.state.correlation_id)

async def validation_error(request, exc):
    return create_error(422, "VALIDATION_ERROR", str(exc), request.state.correlation_id)

async def dependency_unavailable(request, exc):
    return create_error(503, "DEPENDENCY_UNAVAILABLE", str(exc), request.state.correlation_id)

async def internal_error(request, exc):
    return create_error(500, "INTERNAL_ERROR", str(exc), request.state.correlation_id)