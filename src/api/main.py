from fastapi import FastAPI, Request
from src.api.routers.complaints import router as complaints_router
from src.api.routers.customers import router as customer_router
from src.api.routers.health import router as health_router
from src.api.routers.policy import router as policy_router
from data.connection import engine
from data.base import Base
from uuid import uuid4
from src.api.error_handlers.error_handlers import (CustomerNotFoundException, ComplaintNotFoundException, InvalidStatusTransitionException, customer_not_found, complaint_not_found, invalid_status_transition, validation_error, dependency_unavailable, internal_error)
import time
import logging

Base.metadata.create_all(bind=engine) #creates all tables before running application

app = FastAPI() # Get an instance of FastAPI
app.include_router(customer_router)
app.include_router(complaints_router)
app.include_router(policy_router)
app.include_router(health_router) # Adds all the routers to the instance (The endpoints in the router files)
app.add_exception_handler(CustomerNotFoundException, customer_not_found)
app.add_exception_handler(ComplaintNotFoundException, complaint_not_found)
app.add_exception_handler(InvalidStatusTransitionException, invalid_status_transition)
app.add_exception_handler(ValueError, validation_error)
app.add_exception_handler(Exception, internal_error)

logger = logging.getLogger(__name__)

logging.basicConfig(level = logging.INFO,
                    format = (
                        "%(asctime)s %(levelname)s %(message)s"
                    ))

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    correlation_id = str(uuid4())
    request.state.correlation_id = correlation_id

    start = time.time()

    try:
        response = await call_next(request)

        duration_ms = round((time.time() - start) * 1000, 2)

        logger.info(
            f"correlation_id={correlation_id} "
            f"operation={request.method} {request.url.path} "
            f"outcome=success "
            f"duration_ms={duration_ms}"
        )

        response.headers["X-Correlation-ID"] = correlation_id

        return response
    except Exception:
        duration_ms = round((time.time() - start) * 1000, 2)
        logger.error(
            f"correlation_id={correlation_id} "
            f"operation={request.method} {request.url.path} "
            f"outcome=failure "
            f"duration_ms={duration_ms}"
        )

        raise