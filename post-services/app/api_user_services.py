from fastapi import HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
import httpx

import load_envs as _envs


_oauth2schema = OAuth2PasswordBearer(tokenUrl="token")
# NOTE : better be using HTTPBearer() obj instead
# NOTE : LAZY to re-write the current codes, keeps it this way

async def validate_token(token: str = Depends(_oauth2schema)):
    '''
    Use in Depends : Validate User account with a given [token] through User-services, then return [user_id]
    '''
    try:
        _headers = {'Authorization': 'Bearer ' + token}
        res = httpx.post(f"{_envs.USER_SERVICES_URL}/token", headers=_headers)
    except Exception as _error:
        raise HTTPException(status_code=400, detail=f"Error : while sending to User-services >> {str(_error)}")

    # [res_datas] contains either : 'user_id' (SUCCESS) | 'detail' (FAIL)
    _res_datas = res.json()

    if res.status_code != 200:
        #! Error : Connection successed, but no User found
        _error_detail = _res_datas['detail']
        raise HTTPException(status_code=res.status_code, detail=_error_detail)

    return _res_datas['user_id']


async def get_user_views_via_user_token(req: Request):
    '''
    Get User.views of a User, from given token
    '''
    _bearer_and_token = req.headers.get('authorization')

    if _bearer_and_token is None:
        raise HTTPException(status_code=401, detail="Token not receiving")

    try:
        _headers = {'Authorization': _bearer_and_token}
        res = httpx.get(f"{_envs.USER_SERVICES_URL}/views", headers=_headers)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    _res_datas = res.json()

    if res.status_code != 200:
        #! Error : Connection successed, but found Error from User-Services
        _error_detail = _res_datas['detail']
        raise HTTPException(status_code=res.status_code, detail=_error_detail)

    # Return in dict type
    return _res_datas['views']


async def update_views_via_user_token(request: Request, topics_id: list[int]):
    '''
    BACKGROUND TASK : Update Users.[views] in User-services via user TOKEN,  called by getRoomByID()
    '''
    _bearer_and_token = request.headers.get('authorization')
    if _bearer_and_token is not None:
        try:
            _headers = {'Authorization': _bearer_and_token}
            # / Hacky way : set [timeout] to 0.0xx01 to wait a response from the other server
            # /             in a VERY SHORT amount of time.
            httpx.patch(f"{_envs.USER_SERVICES_URL}/views", timeout=0.000000001, headers=_headers, json={ 'topics_id' : topics_id })
        except httpx.TimeoutException:
            pass


async def update_views_via_user_id(user_id: str, topics_id: list[int]):
    '''
    BACKGROUND TASK : Update Users.[views] in User-services via UserID,  called by createRoom() & updateRoom()
    '''
    try:
        httpx.patch(f"{_envs.USER_SERVICES_URL}/views", timeout=0.000000001, json={ 'id': user_id, 'topics_id' : topics_id })
    except httpx.TimeoutException:
        pass