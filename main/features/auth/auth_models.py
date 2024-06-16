import uuid
from datetime import datetime

from sqlalchemy import String, Boolean

from main import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column('id', String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column('email', String(255), nullable=True, unique=True)
    password = db.Column('password', String(255), nullable=True)
    full_name = db.Column('full_name', String(255), nullable=False)
    is_active = db.Column('is_active', Boolean, nullable=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self):
        db.create_all()
