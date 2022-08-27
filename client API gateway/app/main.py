from fastapi import FastAPI

app = FastAPI()

@app.get('/')
async def home():
    return {"API Testing": "Hello FastAPI"}

if __name__ == '__main__':
    import uvicorn

    PORT = 3000

    uvicorn.run("main:app", host='0.0.0.0', port=PORT, reload=True)