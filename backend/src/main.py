from fastapi import FastAPI
import uvicorn

from backend.src.api.athlete import router as athlete_router
from backend.src.api.user import router as user_router

app = FastAPI()

app.include_router(athlete_router)
app.include_router(user_router)

if __name__ == '__main__':
    uvicorn.run('backend.src.main:app', host='localhost', reload=True)