from pathlib import Path

from fastapi import Request, Query
from fastapi.routing import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.src.dependencies import athlete_serviceDP

router = APIRouter(include_in_schema=False, prefix="/athletes")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=f"{BASE_DIR}/frontend/templates/")


@router.get("/", response_class=HTMLResponse)
async def get_all_athletes_html(
        request: Request,
        athlete_service: athlete_serviceDP,
        offset: int = Query(default=0, ge=0, description="Смещение для пагинации"),
        limit: int = Query(default=50, le=100, description="Лимит записей на страницу"),
        ):
    athletes = await athlete_service.get_athletes(offset, limit)

    return templates.TemplateResponse(
        "/athletes/list.html",
        {
            "request": request,
            "athletes": athletes,
            "offset": offset,
            "limit": limit
        }
    )


