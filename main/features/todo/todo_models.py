import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, ForeignKey, DateTime, Column
from sqlalchemy.orm import relationship, backref

from main import db


class Todo(db.Model):
    __tablename__ = 'todo'
    id = Column('id', String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column('user_id', String(36), ForeignKey('user.id'), nullable=False)
    title = Column('title', String(255), nullable=False)
    description = Column('description', String(255), nullable=True)
    date_time = Column('datetime', DateTime, nullable=False)
    is_complete = Column('is_complete', Boolean, default=False)

    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship('User', backref=backref('todos', lazy=True))

    def __init__(self):
        db.create_all()
