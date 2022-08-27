from fastapi import APIRouter, HTTPException

import load_envs as _envs

router = APIRouter()

@router.get('')
async def testRoute():
    return {"TEST":"Hello from POST route"}

@router.get('/test')
async def testConnect():
    import httpx
    try:
        res = httpx.get(f"{_envs.POST_SERVICES_URL}")
        return res.json()
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))