from fastapi import HTTPException
import httpx

import load_envs as _envs

async def get_recommend_topics(user_views: dict) -> dict:
    '''
    Send User.views to Content-Recommend-Services,
    to get a Recommend Dict of topics ID and amount of each topics
    '''
    try:
        res = httpx.post(f"{_envs.CONTENT_RECOMMEND_SERVICES_URL}/", json={ 'views' : user_views})
    except Exception as _error:
        raise HTTPException(status_code=500, detail=str(_error))

    _res_datas = res.json()

    if res.status_code != 200:
        _error_detail = _res_datas['details']
        raise HTTPException(status_code=res.status_code, detail=_error_detail)

    # print("Recommend Topics List: ", _res_datas['views'])

    return _res_datas['views']