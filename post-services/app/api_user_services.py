from fastapi import HTTPException
import httpx

import load_envs as _envs


async def validate_user(user_id: str):
    try:
        res = httpx.get(f"{_envs.USER_SERVICES_URL}/{user_id}")
    except:
        raise Exception("User-services API Error")
    if res.status_code != 200:
        #! Error : Connection successed, but no User found
        _datas = res.json()
        _detail = _datas['detail'] if _datas['detail'] != None else "No response from User API"
        raise Exception(_detail)


async def validate_and_get_user(user_id: str):
    try:
        res = httpx.get(f"{_envs.USER_SERVICES_URL}/{user_id}")
        if res.status_code != 200:
            return None
        user = res.text['user']
        return user
    except:
        raise Exception("API exception")
