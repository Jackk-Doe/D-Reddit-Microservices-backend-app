from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
import api_user_services as _api_users
import schemas as _schemas
import services as _services

# TODO : Update User's interested topics in CREATE & GETONE routes, and send to User-services
# TODO : Put them in BACKGROUND task

# TODO : route to return recommending Room list
# TODO : connect with Content-recommend-services


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
async def getRooms(db: Session = Depends(get_db)):
    return await _services.get_rooms(db=db)

@router.get('/rooms/{room_id}')
async def getRoomByID(room_id: str, db: Session = Depends(get_db)):
    return await _services.get_room_by_id(id=room_id, db=db)

@router.post('/rooms')
async def createRoom(room: _schemas.RoomCreate, db: Session = Depends(get_db), user_id = Depends(_api_users.validate_token)):
    try:
        return await _services.create_room(room=room, user_id=user_id, db=db)
    except Exception as error:
        return HTTPException(status_code=500, detail=str(error))

@router.patch('/rooms/{room_id}')
async def updateRoom(room_id: str, update_room: _schemas.RoomUpdate, db: Session = Depends(get_db), user_id = Depends(_api_users.validate_token)):
    try:
        return await _services.update_room(room_id=room_id, user_id=user_id, update_room=update_room, db=db)
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
    # TODO LATER : Make call to UserServices
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