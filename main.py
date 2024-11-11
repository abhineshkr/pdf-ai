# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddlewarex
from app.db.connection.primary_connection import engine, Base
from app.utils.logger import logger
from app.pdf.router.pdf_to_image_router import convert_to_image_router


# Initialize FastAPI app
app = FastAPI()
app.include_router(convert_to_image_router,tags=["Generic Model Manager"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)