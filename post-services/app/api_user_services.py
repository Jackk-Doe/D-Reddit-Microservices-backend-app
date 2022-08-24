from fastapi import HTTPException
import httpx

import load_envs as _envs

async def validate_user(user_id: str):
    try:
        res = httpx.get(f"{_envs.USER_SERVICES_URL}/{user_id}")
        if res.status_code != 200:
            raise Exception()
    except:
        raise Exception("User-services API Error")
