import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from .api import register_routes
from .database.core import engine, Base
from .logging import configure_logging, LogLevels

load_dotenv()

log_level = os.environ.get("LOG_LEVEL", LogLevels.debug)
log_filename = os.environ.get("LOG_FILENAME", None)
log_filemode = os.environ.get("LOG_FILEMODE", "a")

configure_logging(log_level, filename=log_filename, filemode=log_filemode)

logging.info("DoDoes API is starting up!")
logging.debug(f"Logging configuration: level={log_level}, filename={log_filename}")

app = FastAPI()

""" Only uncomment below to create new tables, 
otherwise the tests will fail if not connected
"""
Base.metadata.create_all(bind=engine)

register_routes(app)
