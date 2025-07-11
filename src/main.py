import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from .logging import configure_logging, LogLevels

load_dotenv()

log_level = os.environ.get("LOG_LEVEL", LogLevels.debug)
log_filename = os.environ.get("LOG_FILENAME", None)
log_filemode = os.environ.get("LOG_FILEMODE", "a")

configure_logging(log_level, filename=log_filename, filemode=log_filemode)

logging.info("DoDoes API is starting up!")
logging.debug(f"Logging configuration: level={log_level}, filename={log_filename}")

app = FastAPI()


@app.get("/")
async def root(request: Request) -> dict:
    logging.debug(f"Handling GET request for {request.url}")
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str, request: Request) -> dict:
    logging.debug(f"Handling GET request for {request.url} with name={name}")
    return {"message": f"Hello {name}"}
