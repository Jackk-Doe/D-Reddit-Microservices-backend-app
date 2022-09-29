from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import HTTPBearer
import httpx

import load_envs as _envs

router = APIRouter()

token_auth_scheme = HTTPBearer(auto_error=False)
# NOTE : [oauth2_scheme] obj looks like this : { scheme = 'Bearer', credentials = 'xxxtokenxxx' }


@router.get('/')
async def testRoute():
    return {"TEST": "Hello from APIGateway : POST route"}


@router.get('/test')
async def testConnect():
    try:
        res = httpx.get(f"{_envs.POST_SERVICES_URL}")
        return res.json()
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.get('/rooms')
async def getRooms(*, recommend: bool = False, token: str = Depends(token_auth_scheme)):
    try:
        if recommend:
            if token is None:
                return HTTPException(status_code=401, detail="Token is required to get Reccomend Rooms")
                
            _headers = {'Authorization': f"Bearer {token.credentials}"}
            res = httpx.get(f"{_envs.POST_SERVICES_URL}/posts/rooms?recommend={recommend}", headers=_headers)
        else:
            res = httpx.get(f"{_envs.POST_SERVICES_URL}/posts/rooms")

        _res = res.json()
        if res.status_code != 200:
            #! Error : Found error from calling service
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.get('/rooms/{room_id}')
async def getById(room_id: int, token: str = Depends(token_auth_scheme)):
    try:
        if token is not None:
            _headers = {'Authorization': f"Bearer {token.credentials}"}
            res = httpx.get(f"{_envs.POST_SERVICES_URL}/posts/rooms/{room_id}", headers=_headers)
        else:
            res = httpx.get(f"{_envs.POST_SERVICES_URL}/posts/rooms/{room_id}")
            
        _res = res.json()
        if res.status_code != 200:
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.post('/rooms')
async def createRoom(payload: dict = Body(example={"room_name": "Room name", "body": "Room body (main text)", "topics": ["beginner", "python"]}), token: str = Depends(token_auth_scheme)):
    try:
        if token is None:
            return HTTPException(status_code=401, detail="Token is required")

        _headers = {'Authorization': f"Bearer {token.credentials}"}
        res = httpx.post(f"{_envs.POST_SERVICES_URL}/posts/rooms", json=payload, headers=_headers)
        _res = res.json()
        if res.status_code != 200:
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.patch('/rooms/{room_id}')
async def updateRoom(room_id: int, payload: dict = Body(example={"room_name": "New Room name", "body": "New Room body (main text)", "topics": ["beginner", "python"]}), token: str = Depends(token_auth_scheme)):
    try:
        if token is None:
            return HTTPException(status_code=401, detail="Token is required")

        _headers = {'Authorization': f"Bearer {token.credentials}"}
        res = httpx.patch(f"{_envs.POST_SERVICES_URL}/posts/rooms/{room_id}", json=payload, headers=_headers)
        _res = res.json()
        if res.status_code != 200:
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.delete('/room/{room_id}')
async def deleteRoom(room_id: int, token: str = Depends(token_auth_scheme)):
    try:
        if token is None:
            return HTTPException(status_code=401, detail="Token is required")

        _headers = {'Authorization': f"Bearer {token.credentials}"}
        res = httpx.delete(f"{_envs.POST_SERVICES_URL}/posts/rooms/{room_id}", headers=_headers)
        _res = res.json()
        if res.status_code != 200:
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.post('/rooms/{room_id}/add-message')
async def addMessage(room_id: int, payload: dict = Body(example={"body": "This is a comment message to add into this Room"}), token: str = Depends(token_auth_scheme)):
    try:
        if token is None:
            return HTTPException(status_code=401, detail="Token is required")

        _headers = {'Authorization': f"Bearer {token.credentials}"}
        res = httpx.post(f"{_envs.POST_SERVICES_URL}/posts/rooms/{room_id}/add-message", json=payload, headers=_headers)
        _res = res.json()
        if res.status_code != 200:
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))