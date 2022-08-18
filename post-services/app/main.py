from fastapi import FastAPI
import os

from database import engine
import models
from router import router

app = FastAPI()

# create table, of not existed
models.Base.metadata.create_all(bind=engine)


@app.get('/')
async def home():
    return {'test': 'Hello World'}

app.include_router(router, prefix="/posts", tags=["posts"])

if __name__ == '__main__':
    import uvicorn
    from dotenv import load_dotenv

    load_dotenv()
    PORT = int(os.getenv('PORT'))

    uvicorn.run("main:app", port=PORT, reload=True)