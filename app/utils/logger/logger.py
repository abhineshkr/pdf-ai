# app/utils/logger.py
from loguru import logger
import os
from dotenv import load_dotenv

load_dotenv()

log_file = os.getenv("LOG_FILE", "app.log")
logger.add(log_file, rotation="1 MB", backtrace=True, diagnose=True)
