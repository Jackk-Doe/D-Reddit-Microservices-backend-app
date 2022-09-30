# NOTE : only the PostgreSQL backend has support for SQL arrays in SQLAlchemy.

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.types import ARRAY
from sqlalchemy.orm import relationship
import datetime

from database import Base


# Association Table : to connect Room & Topic
# NOTE : to use with sqlalchemy relationship(), to created unary direction connection
RoomToTopic_Table = Table(
    "roomtotopic",
    Base.metadata,
    Column("topics_id", ForeignKey("topics.id")),
    Column("rooms_id", ForeignKey("rooms.id")),
)


class Topic(Base):
    __tablename__ = 'topics'

    id = Column(Integer, primary_key=True, index=True)
    topic_name = Column(String)

    def __repr__(self) -> str:
        return f"Topic( id={self.id!r}, topic_name={self.topic_name!r}"


class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String)
    host_id = Column(String)
    body = Column(String)
    participants_id = Column(ARRAY(String), default=[])
    updated = Column(DateTime, default=datetime.datetime.utcnow)
    created = Column(DateTime, default=datetime.datetime.utcnow)

    topics_id = Column(ARRAY(Integer, ForeignKey("topics.id")))

    # TODO LATER (Maybe) : [view] field (INT)

    # topics_id = Column(Integer, ForeignKey("topics.id"))

    # topics = relationship("Topic", foreign_key=[topics_id]) #O2M, Single-direction
    messages = relationship("Message", order_by="Message.created", cascade="all, delete") #O2M, Bi-direction


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id", ondelete="CASCADE"))
    user_id = Column(String)
    body = Column(String)
    updated = Column(DateTime, default=datetime.datetime.utcnow)
    created = Column(DateTime, default=datetime.datetime.utcnow)