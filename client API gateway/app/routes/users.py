from fastapi import APIRouter, HTTPException
import httpx

import load_envs as _envs

router = APIRouter()

@router.get('')
async def testRoute():
    return {"TEST":"Hello from USER route"}


@router.get('/test')
async def testConnection():
    try:
        res = httpx.get(f"{_envs.USER_SERVICES_URL}/")
        return res.json()
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))