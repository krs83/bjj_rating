from fastapi import FastAPI
import uvicorn

from backend.src.api import r_athletes

app = FastAPI()

app.include_router(r_athletes)

if __name__ == '__main__':
    uvicorn.run('backend.src.main:app', host='localhost', reload=True)