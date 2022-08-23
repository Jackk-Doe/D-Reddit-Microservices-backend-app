from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx

from database import SessionLocal
import schemas as _schemas
import services as _services
import load_envs as _env


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
async def createRoom(room: _schemas.RoomCreate, db: Session = Depends(get_db)):
    try:
        response = httpx.get(f"{_env.USER_SERVICES_URL}/{room.host_id}")
        user = response.text

        print("User: ",user)
        print("Statuscode: ",response.status_code != 200)
        
        if response.status_code != 200:
            return {"status_code":401, "detail":"User not found"}
    except:
        return HTTPException(status_code=500, detail="Can not create room")

    return await _services.create_room(room=room, db=db)

# @router.patch('/rooms/{room_id}')
# async def updateRoom(room_id: str):
#     ...
    
@router.delete('/rooms/{room_id}')
async def deleteRoom(room_id: str, db: Session = Depends(get_db)):
    # TODO : Make call to UserServices
    await _services.delete_room(id=room_id, db=db)
    return {"status_code": 200}

@router.post('/rooms/{room_id}/add-message')
async def addMessage(room_id: int, message: _schemas.MessageCreate, db: Session = Depends(get_db)):
    # TODO : Make call to UserServices
    return await _services.add_message_to_room(room_id=room_id, message=message, db=db)


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
    # TODO : Make call to UserServices
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