from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.security import HTTPBearer
import httpx

import load_envs as _envs

router = APIRouter()

token_auth_scheme = HTTPBearer(auto_error=False)
# NOTE : [oauth2_scheme] obj looks like this : { scheme = 'Bearer', credentials = 'xxxtokenxxx' }


@router.get('/')
async def testRoute():
    '''
    Test POST-related routes of the custom API Gateway
    '''
    return {"TEST": "Hello from APIGateway : POST route"}


@router.get('/test')
async def testConnect():
    '''
    Test API connection, by sending request to the POST Services
    '''
    try:
        res = httpx.get(f"{_envs.POST_SERVICES_URL}")
        return res.json()
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.get('/rooms')
async def getRooms(*, recommend: bool = False, token: str = Depends(token_auth_scheme)):
    '''
    Get all Rooms. with avialable query string parameters : 
    - **recommend**: to get backend generating Recommend Rooms, generate from User's interested (viewed) topics, **Bearer Token** is required
    '''
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
    '''
    Get a Room by its ID,

    if passing **Bearer token** with this request, record this Room topics into User' view history
    \f
    '''
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
    """
    Create a Room with all the information:

    - **room_name**: a name of this new Room
    - **body**: a long description
    - **topics**: a list of topics about this Room

    - **Bearer token for authenication** 

    Also update User's interested topics, from topics of this Room
    \f
    """
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
    """
    Update a Room with all the information:

    NOTE : Only a Room owner can update a person's Room

    - **room_id**: an ID of a update Room

    - **room_name**: an updating name of this new Room
    - **body**: an updating long description
    - **topics**: an updating list of topics about this Room

    - **Bearer token for authenication** 

    Also update User's interested topics, from topics of this Room (if topics changed)
    \f
    """
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
    '''
    Delete a Room by its ID,

    - **Bearer token for authenication** 

    NOTE : Only a Room owner can delete a person's Room
    \f
    '''
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
    """
    Add comment (messages) to a Room

    NOTE : User must has an account to add (post) comment 

    - **room_id**: an ID of a update Room
    - **Bearer token for User account validation** 

    \f
    """
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