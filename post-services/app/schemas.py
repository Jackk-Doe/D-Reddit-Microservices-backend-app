from datetime import datetime
from pydantic import BaseModel


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
    room_id: int
    user_id: int

    class Config:
        orm_mode = True

class Message(MessageCreate):
    id: int
    updated: datetime
    created: datetime

    class Config:
        orm_mode = True


# Room Schemas
class _RoomBase(BaseModel):
    room_name: str
    host_id: int
    body: str
    

class RoomCreate(_RoomBase):
    topics: list[str]
    
    class Config:
        orm_mode = True

class Room(_RoomBase):
    id: int
    topic_ids: list[int]
    participants_id: list[int]
    messages: list[Message]
    updated: datetime
    created: datetime

    class Config:
        orm_mode = True