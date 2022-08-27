from fastapi import FastAPI

import load_envs as _envs

app = FastAPI()

@app.get('/')
async def home():
    return {"API Testing": "Hello FastAPI"}

if __name__ == '__main__':
    import uvicorn

    PORT = int(_envs.PORT)

    # NOTE : Need to specify [host] param in uvicorn.run(), else Not getting any reply from server, when in Docker
    uvicorn.run("main:app", host='0.0.0.0', port=PORT, reload=True)