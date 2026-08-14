from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import router
from src.logging.logger import Logger, ErrorLogger


app = FastAPI(
    title="Get-My-Doc",
    version="0.1.0",
)
Logger().info("Backend app created")

app.include_router(router)
Logger().info("app router set")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
Logger().info("app CORSMiddleware set")