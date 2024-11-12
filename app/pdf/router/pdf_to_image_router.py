from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.utils.logger import logger
from app.pdf.services.pdf_to_image_service import process_pdf_to_images
from typing import List

# Define a router object
convert_to_image_router = APIRouter()

@convert_to_image_router.post("/convert/pdf/images")
async def convert_pdf_to_images_endpoint(
    files: List[UploadFile] = File(...),  # Handle multiple PDF files
    max_pages: int = 0,
    skip_first_n_pages: int = 0
):
    #try:
        # Delegate PDF processing to the service layer
        image_files_per_pdf = process_pdf_to_images(files, max_pages, skip_first_n_pages)

        return JSONResponse(content={"result": image_files_per_pdf, "message": "PDFs successfully converted to images"})

    #except Exception as e:
        #logger.error(f"Error converting PDF to images: {e}")
        #raise HTTPException(status_code=500, detail="An error occurred while processing the PDF files.")
