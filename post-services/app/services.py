from sqlalchemy.orm import Session
from fastapi import HTTPException

import database as _database
import schemas as _schemas
import models as _models


"""
Room Routes 
"""


async def get_rooms(db: Session):
    return [_schemas.Room.from_orm(_rooms) for _rooms in db.query(_models.Room).all()]


async def get_room_by_id(id: int, db: Session):
    _room = db.query(_models.Room).get(id)
    if not _room:
        raise HTTPException(status_code=404, detail="Given room id not found")
    return _schemas.Room.from_orm(_room)


async def create_room(room: _schemas.RoomCreate, db: Session):

    async def check_topics_exist(topic: str) -> int:
        '''
        If existed return, else create new Topic
        '''
        topic_search: _models.Topic = db.query(
            _models.Topic).filter_by(topic_name=topic).first()
        if topic_search:
            return topic_search.id
        else:
            _topic = _models.Topic(topic_name=topic)
            db.add(_topic)
            db.commit()
            db.refresh(_topic)
            return _topic.id

    _topic_ids = [await check_topics_exist(topic) for topic in room.topics]
    _room = _models.Room(room_name=room.room_name,
                         host_id=room.host_id, body=room.body, topic_ids=_topic_ids)
    db.add(_room)
    db.commit()
    db.refresh(_room)
    return _schemas.Room.from_orm(_room)


async def delete_room(id: int, db: Session):
    _room = db.query(_models.Room).get(id)
    if not _room:
        raise HTTPException(
            status_code=404, detail="The given room id not found")
    db.delete(_room)
    db.commit()


async def add_message_to_room(room_id: int, message: _schemas.MessageCreate, db: Session):
    _room = db.query(_models.Room).get(room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail="The given room id not found")
    _message = _models.Message(
        body=message.body, user_id=message.user_id, room_id=room_id)
    db.add(_message)
    db.commit()
    db.refresh(_message)
    return _schemas.Room.from_orm(_room)

"""
Messages Routes 
"""


async def get_messages(db: Session):
    return [_schemas.Message.from_orm(_messages) for _messages in db.query(_models.Message).all()]


# async def create_message(message: _schemas.MessageCreate, db: Session):
#     try:
#         _message = _models.Message(**message.dict())
#         db.add(_message)
#         db.commit()
#         db.refresh(_message)
#         return _schemas.Message.from_orm(_message)
#     except:
#         db.rollback()
#         raise HTTPException(status_code=404, detail="Fail to add new Message")


async def delete_message(message_id: int, db: Session):
    _message = db.query(_models.Message).get(message_id)
    if not _message:
        raise HTTPException(
            status_code=404, detail="Given message id for delete not found")
    db.delete(_message)
    db.commit()


"""
Topics Routes 
"""


async def get_topics(db: Session):
    return [_schemas.Topic.from_orm(_topic) for _topic in db.query(_models.Topic).all()]


async def create_topic(topic: _schemas.TopicCreate, db: Session):
    _topic = _models.Topic(**topic.dict())
    db.add(_topic)
    db.commit()
    db.refresh(_topic)
    return _schemas.Topic.from_orm(_topic)
