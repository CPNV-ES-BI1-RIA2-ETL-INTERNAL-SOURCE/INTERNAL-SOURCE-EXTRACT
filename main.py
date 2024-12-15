from fastapi import FastAPI

from app.endpointController import api_router

app = FastAPI()

app.include_router(api_router)