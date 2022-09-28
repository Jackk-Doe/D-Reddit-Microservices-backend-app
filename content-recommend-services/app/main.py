from fastapi import FastAPI
from pydantic import BaseModel

import load_env as _envs

app = FastAPI()

class UserInterest(BaseModel):
    views : dict[int, int]


@app.get('/test')
async def testRoute():
    return {'test': 'Hello World From Content-Filter-Services'}


@app.post('/')
async def getRoomRecommend(datas: UserInterest):
    '''
    This function is : f(a) = b 
    where [a] is Dict[int,int] of : User interested topics ID]
    and [b] is Dict[int,int] of   : Recommending topics ID for the User ]
    '''

    _views = datas.views
    _total_views = sum(_views.values())

    _recommend_topics = {}

    for _topic_id, _view_count in _views.items():
        _recomm_num = round((_view_count/_total_views) * 10)
        if _recomm_num != 0:
            _recommend_topics[_topic_id] = _recomm_num

    # NOTE : approximately return 10 recommending topics ID
    return { 'views': _recommend_topics }


if __name__ == '__main__':
    import uvicorn

    PORT = int(_envs.PORT)
    uvicorn.run("main:app", port=PORT, host='0.0.0.0', reload=True)