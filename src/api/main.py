from fastapi import FastAPI
from src.api.routers.complaints import router as complaints_router
from src.api.routers.customers import router as customer_router
from src.api.routers.health import router as health_router
from data.connection import engine
from data.base import Base

Base.metadata.create_all(bind=engine) #creates all tables before running application
app = FastAPI() # Get an instance of FastAPI
app.include_router(customer_router)
app.include_router(complaints_router)
app.include_router(health_router) # Adds all the routers to the instance (The endpoints in the router files)

