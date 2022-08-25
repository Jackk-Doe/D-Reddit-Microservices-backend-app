from datetime import datetime
from pydantic import BaseModel
from typing import Union


# Topic Schemas
class _TopicBase(BaseModel):
    topic_name: str

class TopicCreate(_TopicBase):

    class Config:
        orm_mode = True

class Topic(_TopicBase):
    id: int

    class Config:
        orm_mode = True


# Message Schemas
class _MessageBase(BaseModel):
    body: str

class MessageCreate(_MessageBase):
    class Config:
        orm_mode = True

class Message(MessageCreate):
    id: int
    user_id: str
    room_id: int
    updated: datetime
    created: datetime

    class Config:
        orm_mode = True


# Room Schemas
class _RoomBase(BaseModel):
    room_name: str
    body: str
    

class RoomCreate(_RoomBase):
    topics: list[str]
    
    class Config:
        orm_mode = True

class Room(_RoomBase):
    id: int
    host_id: str
    topics_id: list[int]
    participants_id: list[str]
    messages: list[Message]
    updated: datetime
    created: datetime

    class Config:
        orm_mode = True

class RoomUpdate(RoomCreate):
    pass