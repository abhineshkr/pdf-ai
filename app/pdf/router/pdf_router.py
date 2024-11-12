# routers/pdf_router.py

from fastapi import APIRouter, UploadFile, File, Depends
from typing import List


pdf_parser_router = APIRouter()

class PDFHandler:
    def __init__(self, model_list):
        self.model_list = model_list

    def process_pdf(self, pdf_file):
        # Use self.model_list for processing
        return {"message": "PDF processed", "model_list": self.model_list}
    
@pdf_parser_router.get("/")
def server():
    return {"message": "Welcome to Marker-api"}

@pdf_parser_router.post("/convert")
async def convert_pdf_to_markdown(pdf_file: UploadFile):
    """
    Endpoint to convert a single PDF to markdown.
    Args:
    pdf_file (UploadFile): The uploaded PDF file.
    Returns:
    dict: The response from processing the PDF file.
    """
    file = await pdf_file.read()
    response = process_pdf_file(file, pdf_file.filename)  # Pass model_list
    return [response]

@pdf_parser_router.post("/batch_convert")
async def convert_pdfs_to_markdown(pdf_files: List[UploadFile] = File(...)):
    """
    Endpoint to convert multiple PDFs to markdown.
    Args:
    pdf_files (List[UploadFile]): The list of uploaded PDF files.
    Returns:
    list: The responses from processing each PDF file.
    """
    async def process_files(files):
        return [await process_pdf_file(await file.read(), file.filename) for file in files]

    responses = await process_files(pdf_files)
    return responses
