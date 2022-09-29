from fastapi import APIRouter, HTTPException, Body
import httpx

import load_envs as _envs

router = APIRouter()

@router.get('/')
async def testRoute():
    '''
    Test User-related routes of the custom API Gateway
    '''
    return {"TEST":"Hello from APIGateway : USER route"}


@router.get('/test')
async def testConnection():
    '''
    Test API connection, by sending request to the USER Services
    '''
    try:
        res = httpx.get(f"{_envs.USER_SERVICES_URL}/")
        return res.json()
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.post('/signup')
async def signupUser(payload: dict = Body(example={"name": "User name (e.g: Jackk Doe)", "email": "User email here", "password": "User password here", "bio": "About User bio"})):
    '''
    Sign up with [name], [email], [password], [bio] to create User account,
    to receive User account datas and [token] from User-Services
    '''
    try:
        res = httpx.post(f"{_envs.USER_SERVICES_URL}/users/signup", json=payload)
        _res = res.json()
        if res.status_code != 201:
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))


@router.post('/signin')
async def signinUser(payload: dict = Body(example={"email": "User email here", "password": "User password here"})):
    '''
    Sign in with [email] & [password] to recieve User account datas,
    thus receive [name], [email], [bio], & [token] from User-Services
    '''
    try:
        res = httpx.post(f"{_envs.USER_SERVICES_URL}/users/signin", json=payload)
        _res = res.json()
        if res.status_code != 200:
            return {'status_code': res.status_code, 'detail': _res['detail']}
        return _res
    except Exception as _error:
        return HTTPException(status_code=500, detail=str(_error))