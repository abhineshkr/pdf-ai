# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
#from fastapi.middleware.cors import CORSMiddlewarex
from app.db.connection.primary_connection import engine, Base
from app.utils.logger import logger
from app.pdf.router.pdf_router import pdf_parser_router
from app.pdf.dependencies import access_list_dependency
 
# Global variable to hold model list



# Event that runs on startup to load all models
'''
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.debug("--------------------- Loading OCR Model -----------------------")
    app.state.model_list = load_all_models()  # Load your models into app state
    yield  # Yield control back to the app, allowing it to run
    
    #logger.debug("--------------------- Unloading OCR Model -----------------------")
    #app.state.model_list = None  # Clean up if necessary
'''



# Initialize FastAPI app
app = FastAPI()

# Add CORS middleware to allow cross-origin requests
#app.add_middleware( CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True)


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await access_list_dependency()



# Include the router
app.include_router(pdf_parser_router, prefix="/pdf/parser", tags=["pdf"])

def main():
    #parser = argparse.ArgumentParser(description="Run the marker-api server.")
    #parser.add_argument("--host", default="0.0.0.0", help="Host IP address")
    #parser.add_argument("--port", type=int, default=8000, help="Port number")
    #args = parser.parse_args()
    uvicorn.run(app, host=args.host, port=args.port)

if __name__ == "__main__":
    main()
