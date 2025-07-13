import logging
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

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

app = FastAPI(
    title="DoDoes API",
    summary="A modern backend service for managing tasks and user authentication.",
    description="""
This API provides endpoints for secure user authentication and flexible todo task management.

Features include:
- OAuth2-based login with JWT tokens
- User profile and credential handling
- Creation, update, and completion of todos with priority and due dates
- Robust rate limiting and structured error responses

Ideal for integration into frontend applications or as a standalone backend.
""",
    version="1.0.0",
    contact={"name": "Jakub Niewiarowski", "GitHub": "https://github.com/Niewiaro"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"}
)

# Mount only static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve index.html manually for "/"
@app.get("/", response_class=HTMLResponse)
async def serve_root() -> str:
    with open("static/index.html") as f:
        return f.read()

"""
Only uncomment below to create new tables, 
otherwise the e2e tests will fail if not connected
"""
# Base.metadata.create_all(bind=engine)

register_routes(app)
