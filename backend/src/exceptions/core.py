from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from backend.src.config import settings

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/frontend/templates/")


def not_found_error(request: Request, exc: HTTPException):
    return templates.TemplateResponse(
        "errors/404.html",
        {"request": request,
         "status_code": exc.status_code,
         "detail": exc.detail,
         "site_name": settings.SITENAME,
         "current_year": settings.current_year,
         "header_image": settings.HEADER_IMAGE,}
    )