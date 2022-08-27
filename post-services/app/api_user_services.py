from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
import httpx

import load_envs as _envs


_oauth2schema = OAuth2PasswordBearer(tokenUrl="token")

async def validate_token(token: str = Depends(_oauth2schema)):
    '''
    Validate User account with a given [token] through User-services, then return [user_id]
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
