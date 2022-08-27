from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import OAuth2PasswordBearer
import httpx

import load_envs as _envs

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get('/')
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
        _res = res.json()
        if res.status_code != 200:
            #! Error : Found error from calling service
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=_error)


@router.get('/rooms/{room_id}')
async def getById(room_id: int):
    try:
        res = httpx.get(f"{_envs.POST_SERVICES_URL}/posts/rooms/{room_id}")
        _res = res.json()
        if res.status_code != 200:
            #! Error
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.post('/rooms')
async def createRoom(payload: dict = Body(), token: str = Depends(oauth2_scheme)):
    try:
        _headers = {'Authorization': 'Bearer ' + token}
        res = httpx.post(f"{_envs.POST_SERVICES_URL}/posts/rooms", json=payload, headers=_headers)
        _res = res.json()
        if res.status_code != 200:
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))