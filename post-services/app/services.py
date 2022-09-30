from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import array
from fastapi import HTTPException
from datetime import datetime

import database as _database
import schemas as _schemas
import models as _models


"""
Room Routes 
"""


async def get_rooms(db: Session):
    return [_schemas.Room.from_orm(_rooms) for _rooms in db.query(_models.Room).all()]


async def get_recommend_rooms(recommend_topics: dict[int,int],db: Session):
    _recommend_rooms = []

    for _topic_id, _count in recommend_topics.items():
        _rooms = db.query(_models.Room).filter(_models.Room.topics_id.any_() == _topic_id).limit(_count).all()

        # NOTE : flatten [_rooms] before adding into list
        [_recommend_rooms.append(_room) for _room in _rooms if _room not in _recommend_rooms]

    return [_schemas.Room.from_orm(_room) for _room in _recommend_rooms]


async def get_room_by_id(id: int, db: Session):
    _room = db.query(_models.Room).get(id)
    if not _room:
        raise HTTPException(status_code=404, detail="Given room id not found")
    return _schemas.Room.from_orm(_room)


async def _create_or_return_one_topic(topic: str, db: Session) -> _models.Topic:
    '''
    Helper func : If existed return, else create new Topic in DB
    '''
    topic_search: _models.Topic = db.query(
        _models.Topic).filter_by(topic_name=topic).first()
    if topic_search:
        return topic_search
    else:
        _topic = _models.Topic(topic_name=topic)
        db.add(_topic)
        db.commit()
        db.refresh(_topic)
        return _topic


async def create_room(room: _schemas.RoomCreate, user_id: str, db: Session):
    _topics = [await _create_or_return_one_topic(topic, db) for topic in room.topics]
    # Convert [room.topics] to List[int]
    _topics_id = [_topic.id for _topic in _topics]
    _room = _models.Room(room_name=room.room_name,
                         host_id=user_id, body=room.body, topics_id=_topics_id, topics=_topics)
    db.add(_room)
    db.commit()
    db.refresh(_room)
    return _schemas.Room.from_orm(_room)


async def update_room(room_id: int, user_id: str, update_room: _schemas.RoomUpdate, db: Session):
    _current_room: _models.Room = db.query(_models.Room).get(room_id)
    if not _current_room:
        #! Error : Room not found
        raise HTTPException(status_code=404, detail="The given room id not found")

    if _current_room.host_id != user_id:
        #! Error : This userID does not own this room
        raise HTTPException(
            status_code=403, detail="The user does not own this room, to update")

    # Convert [room.topics] to List[int]
    topics = [await _create_or_return_one_topic(topic, db) for topic in update_room.topics]
    topics_id = [_topic.id for _topic in topics]

    # Create dict
    _update_room_data = update_room.dict(exclude_unset=True)
    # Remove [topics], which is List[str] from dict
    del _update_room_data['topics']

    # Add necessary fields, to do update
    _update_room_data['topics'] = topics
    _update_room_data['topics_id'] = topics_id
    _update_room_data['updated'] = datetime.utcnow()

    # NOTE : Get new topics ID from the update datas
    #        To use in User.views updating
    _new_topics_id = [_new_topic for _new_topic in topics_id if _new_topic not in _current_room.topics_id]

    #/ Update fields that are different from the current data of [_current_room]
    for key, value in _update_room_data.items():
        setattr(_current_room, key, value)

    db.add(_current_room)
    db.commit()
    db.refresh(_current_room)
    return _schemas.Room.from_orm(_current_room), _new_topics_id


async def delete_room(id: int, user_id: str, db: Session):
    _room = db.query(_models.Room).get(id)
    if not _room:
        #! Error : Room not found
        raise HTTPException(
            status_code=404, detail="The given room id not found")
    if _room.host_id != user_id:
        #! Error : This userID does not own this room
        raise HTTPException(
            status_code=403, detail="The user does not own this room, to delete")

    db.delete(_room)
    db.commit()


async def add_message_to_room(room_id: int, user_id: str, message: _schemas.MessageCreate, db: Session):
    _room = db.query(_models.Room).get(room_id)
    if not _room:
        raise HTTPException(
            status_code=404, detail="The given room id not found")
    _message = _models.Message(
        body=message.body, user_id=user_id, room_id=room_id)
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
