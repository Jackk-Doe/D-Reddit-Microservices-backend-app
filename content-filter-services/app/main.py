from fastapi import FastAPI

app = FastAPI()

@app.get('/test')
async def testRoute():
    return {'test': 'Hello World From Content-Filter-Services'}


if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", port=8080, host='0.0.0.0', reload=True)