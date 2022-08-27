from fastapi import APIRouter, HTTPException
import httpx

import load_envs as _envs

router = APIRouter()


@router.get('')
async def testRoute():
    return {"TEST": "Hello from POST route"}


@router.get('/test')
async def testConnect():
    try:
        res = httpx.get(f"{_envs.POST_SERVICES_URL}")
        return res.json()
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.get('/rooms')
async def getRooms():
    try:
        res = httpx.get(f"{_envs.POST_SERVICES_URL}/posts/rooms")
        _res_datas = res.json()
        if res.status_code is not 200:
            #! Error : Found error from calling service
            return {'status_code': res.status_code, 'detail': _res_datas['detail']}
        return _res_datas
    except Exception as _error:
        return HTTPException(status_code=500, detail=_error)
