from fastapi import FastAPI
import uvicorn

from backend.src.api.athlete import router as athlete_router
from backend.src.api.user import router as user_router
from backend.src.api.auth import router as auth_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(athlete_router)

if __name__ == '__main__':
    uvicorn.run('backend.src.main:app', host='localhost', reload=True)