from fastapi import FastAPI

import load_env as _envs

app = FastAPI()

@app.get('/test')
async def testRoute():
    return {'test': 'Hello World From Content-Filter-Services'}


if __name__ == '__main__':
    import uvicorn

    PORT = int(_envs.PORT)
    uvicorn.run("main:app", port=PORT, host='0.0.0.0', reload=True)