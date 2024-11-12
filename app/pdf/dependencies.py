# dependencies.py
from fastapi import FastAPI
from app.pdf.model.models import load_all_models  # Import function to load models

# Global variable to hold the access list
access_list = []

# Dependency to access the global access list
async def access_list_dependency():
    access_list = load_all_models();
    return access_list 
