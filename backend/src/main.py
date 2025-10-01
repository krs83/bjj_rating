from fastapi import FastAPI
import uvicorn

from backend.src.api.athlete import router as athlete_router
from backend.src.api.user import router as user_router
from backend.src.api.auth import router as auth_router
from backend.src.admin.setup import setup_admin
from backend.src.config import settings

app = FastAPI()

setup_admin(app)

app.include_router(auth_router, prefix=settings.API_V1_STR)
app.include_router(user_router)
app.include_router(athlete_router)

if __name__ == '__main__':
    uvicorn.run('backend.src.main:app', host='localhost', reload=True)