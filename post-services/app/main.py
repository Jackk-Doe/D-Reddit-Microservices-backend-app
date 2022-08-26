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

    # NOTE : Need to specify [host] param in uvicorn.run(), else Not getting any reply from server, when in Docker
    uvicorn.run("main:app", host='0.0.0.0', port=PORT, reload=True)