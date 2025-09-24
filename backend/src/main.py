from fastapi import FastAPI
import uvicorn

app = FastAPI()


if __name__ == '__main__':
    uvicorn.run('backend.app.main', host='localhost', reload=True)