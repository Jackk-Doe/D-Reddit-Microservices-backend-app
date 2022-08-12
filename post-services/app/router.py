from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
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
async def getRooms(db: Session = Depends(get_db)):
    return await _services.get_rooms(db=db)

# @router.get('/rooms/{room_id}')
# async def getOne(room_id: str):
#     ...

@router.post('/rooms')
async def createRoom(room: _schemas.RoomCreate, db: Session = Depends(get_db)):
    return await _services.create_room(room=room, db=db)

# @router.patch('/rooms/{room_id}')
# async def updateRoom(room_id: str):
#     ...
    
# @router.delete('/rooms/{room_id}')
# async def deleteRoom(room_id: str):
#     ...


'''
Messages Routes 
'''
@router.get('/messages', response_model=List[_schemas.Message])
async def getMessages(db: Session = Depends(get_db)):
    return await _services.get_messages(db=db)

@router.post('/messages', response_model=_schemas.Message)
async def createMessage(message: _schemas.MessageCreate, db: Session = Depends(get_db)):
    return await _services.create_message(message=message, db=db)

@router.delete('/messages/{message_id}')
async def deleteMessage(message_id: int, db: Session = Depends(get_db)):
    return await _services.delete_message(message_id=message_id, db=db)


'''
Topics Routes 
'''
@router.get('/topics', response_model=List[_schemas.Topic])
async def getTopics(db: Session = Depends(get_db)):
    return await _services.get_topics(db=db)

@router.post('/topics', response_model=_schemas.Topic)
async def createTopic(topic: _schemas.TopicCreate, db: Session = Depends(get_db)):
    return await _services.create_topic(topic=topic, db=db)