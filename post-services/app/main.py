from fastapi import FastAPI

from database import engine
from router import router
import load_envs as _envs
import models

app = FastAPI()

# create table, of not existed
models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def home():
    return {'test': 'Hello World'}

app.include_router(router, prefix="/posts", tags=["posts"])

if __name__ == '__main__':
    import uvicorn

    PORT = int(_envs.PORT)

    uvicorn.run("main:app", port=PORT, reload=True)