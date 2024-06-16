import datetime
from typing import Any

import jwt

from main import db, settings, login_manager
from main.features.auth.auth_models import User
import requests


class AuthServices:
    # Flask-Login helper to retrieve a user from our db
    @staticmethod
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()

    @staticmethod
    def get_google_provider_cfg():
        return requests.get(settings.GOOGLE_DISCOVERY_URL).json()

    @staticmethod
    def create_user(user_vo):
        db.session.add(user_vo)
        db.session.commit()

    @staticmethod
    def get_user(user_vo: User) -> Any | None:
        user = User.query.filter(User.email == user_vo.email, User.password == user_vo.password).all()
        if user:
            return user[0]
        else:
            return None

    @staticmethod
    def get(unique_id):
        user = User.query.filter(User.id == unique_id).all()
        if user:
            return user[0]
        else:
            return None

    @staticmethod
    def encode_auth_token(user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30, seconds=0),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, settings.JWT_SECRET_KEY, algorithms=settings.JWT_ALGORITHM)
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
