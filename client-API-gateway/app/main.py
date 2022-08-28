from fastapi import FastAPI

import load_envs as _envs
from routes.posts import router as _post_router
from routes.users import router as _user_router


app = FastAPI()

# Includes router to Post and User
app.include_router(_post_router, prefix="/posts")
app.include_router(_user_router, prefix="/users")

@app.get('/')
async def home():
    return {"API Testing": "Hello FastAPI From API Gateway"}

if __name__ == '__main__':
    import uvicorn

    PORT = int(_envs.PORT)

    # NOTE : Need to specify [host] param in uvicorn.run(), else Not getting any reply from server, when in Docker
    uvicorn.run("main:app", host='0.0.0.0', port=PORT, reload=True)