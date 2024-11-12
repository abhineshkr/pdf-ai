import os
import traceback
from typing import List
from app.utils.logger import logger
from PIL import Image
from pdf2image import convert_from_path
from fastapi import UploadFile

PDF_PROCESS_IMAGE_PATH = os.getenv("PDF_PROCESS_IMAGE_PATH", "D:/LLM/models/")

def convert_pdf_to_images(input_pdf_file_path: str, max_pages: int = 0, skip_first_n_pages: int = 0) -> List[Image.Image]:
    #logger.info(f"Processing PDF file {input_pdf_file_path}")
    if max_pages == 0:
        last_page = None
        #logger.info("Converting all pages to images...")
    else:
        last_page = skip_first_n_pages + max_pages
        #logger.info(f"Converting pages {skip_first_n_pages + 1} to {last_page}")
    
    first_page = skip_first_n_pages + 1  # pdf2image uses 1-based indexing
    #try:
    images = convert_from_path(input_pdf_file_path, first_page=first_page, last_page=last_page)
    #logger.info(f"Converted {len(images)} pages from PDF file to images.")
    #except Exception as e:
        ##logger.error(f"Failed to convert PDF to images: {e}")
        #raise

    return images

def process_pdf_to_images(files: List[UploadFile], max_pages: int, skip_first_n_pages: int) -> List[dict]:
    image_files_per_pdf = []
    save_directory = PDF_PROCESS_IMAGE_PATH

    # Ensure the save directory exists
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    #try:
    for file in files:
        ##logger.info(f"Processing file: {file.filename}")
        # Save uploaded PDF temporarily
        input_pdf_file_path = f"temp_{file.filename}"
        with open(input_pdf_file_path, "wb") as pdf_file:
            pdf_file.write(file.file.read())

        # Convert the PDF to images
        images = convert_pdf_to_images(input_pdf_file_path, max_pages, skip_first_n_pages)

        # Save images in the specified directory
        image_files = []
        for idx, img in enumerate(images):
            image_path = os.path.join(save_directory, f"{file.filename}_{idx}.png")
            img.save(image_path)
            image_files.append(image_path)

        # Append image files for the current PDF
        image_files_per_pdf.append({
            "pdf": file.filename,
            "images": image_files
        })

        # Clean up the uploaded PDF
        os.remove(input_pdf_file_path)

    return image_files_per_pdf

    #except Exception as e:
        ##logger.error(f"Error processing PDF files: {e}\n{traceback.format_exc()}")
        #raise e
