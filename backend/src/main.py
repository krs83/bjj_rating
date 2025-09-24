from fastapi import FastAPI
import uvicorn

app = FastAPI()


if __name__ == '__main__':
    uvicorn.run('backend.src.main:app', host='localhost', reload=True)