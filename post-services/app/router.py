from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
import api_user_services as _api_users
import api_content_recommend_services as _api_c_recom
import schemas as _schemas
import services as _services


router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''
Room Routes 
'''
@router.get('/rooms', response_model=List[_schemas.Room])
async def getRooms(*, recommend: bool = False ,db: Session = Depends(get_db), request: Request):
    if recommend:
        #/ Send system-recommend Rooms to user, base on User.views (interested)
        _user_views = await _api_users.get_user_views_via_user_token(req=request)
        print("User views datas: ", _user_views)
        _recommend_topics_id = await _api_c_recom.get_recommend_topics(user_views=_user_views)
        print("Recommend Topics ID list: ", _recommend_topics_id)
        return await _services.get_recommend_rooms(recommend_topics=_recommend_topics_id, db=db)

    return await _services.get_rooms(db=db)

@router.get('/rooms/{room_id}')
async def getRoomByID(*, room_id: str, db: Session = Depends(get_db), background_tasks: BackgroundTasks, request: Request):
    _room = await _services.get_room_by_id(id=room_id, db=db)
    if _room.topics_id:
        # NOTE : Only update if [_room.topics_id] is not empty
        # If the [request] contains token, run a background task to send request to User-services,
        # to update User.views (User's interested), by the topics_id of this [_room]
        background_tasks.add_task(_api_users.update_views_via_user_token, request, _room.topics_id)
    return _room

@router.post('/rooms')
async def createRoom(*, room: _schemas.RoomCreate, db: Session = Depends(get_db), user_id = Depends(_api_users.validate_token), background_tasks: BackgroundTasks):
    try:
        _room = await _services.create_room(room=room, user_id=user_id, db=db)
        if _room.topics_id: 
            # NOTE : Only update if [_room.topics_id] is not empty
            background_tasks.add_task(_api_users.update_views_via_user_id, user_id, _room.topics_id)
        return _room
    except Exception as error:
        return HTTPException(status_code=500, detail=str(error))

@router.patch('/rooms/{room_id}')
async def updateRoom(*, room_id: str, update_room: _schemas.RoomUpdate, db: Session = Depends(get_db), user_id = Depends(_api_users.validate_token), background_tasks: BackgroundTasks):
    try:
        _room, _new_topics_id = await _services.update_room(room_id=room_id, user_id=user_id, update_room=update_room, db=db)
        if _new_topics_id:
            # NOTE : Only update if [_new_topics_id] is not empty
            background_tasks.add_task(_api_users.update_views_via_user_id, user_id, _new_topics_id)
        return _room
    except HTTPException as _http_error:
        return HTTPException(status_code=_http_error.status_code, detail=_http_error.detail)
    except Exception as error:
        return HTTPException(status_code=500, detail=str(error))
    
@router.delete('/rooms/{room_id}')
async def deleteRoom(room_id: str, db: Session = Depends(get_db), user_id = Depends(_api_users.validate_token)):
    try:
        await _services.delete_room(id=room_id, user_id=user_id, db=db)
        return {"status_code": 200}
    except HTTPException as _http_error:
        return HTTPException(status_code=_http_error.status_code, detail=_http_error.detail)
    except Exception as error:
        return HTTPException(status_code=500, detail=str(error))

@router.post('/rooms/{room_id}/add-message')
async def addMessage(room_id: int, message: _schemas.MessageCreate, db: Session = Depends(get_db), user_id = Depends(_api_users.validate_token)):
    try:
        return await _services.add_message_to_room(room_id=room_id, user_id=user_id, message=message, db=db)
    except HTTPException as _http_error:
        return HTTPException(status_code=_http_error.status_code, detail=_http_error.detail)
    except Exception as error:
        return HTTPException(status_code=500, detail=str(error))


'''
Messages Routes 
'''
@router.get('/messages', response_model=List[_schemas.Message])
async def getMessages(db: Session = Depends(get_db)):
    return await _services.get_messages(db=db)

# @router.post('/messages', response_model=_schemas.Message)
# async def createMessage(message: _schemas.MessageCreate, db: Session = Depends(get_db)):
#     return await _services.create_message(message=message, db=db)

@router.delete('/messages/{message_id}')
async def deleteMessage(message_id: int, db: Session = Depends(get_db)):
    # TODO LATER (Maybe) : Make call to UserServices
    await _services.delete_message(message_id=message_id, db=db)
    return {"status_code": 200}


'''
Topics Routes 
'''
@router.get('/topics', response_model=List[_schemas.Topic])
async def getTopics(db: Session = Depends(get_db)):
    return await _services.get_topics(db=db)

@router.post('/topics', response_model=_schemas.Topic)
async def createTopic(topic: _schemas.TopicCreate, db: Session = Depends(get_db)):
    return await _services.create_topic(topic=topic, db=db)