from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from .models import User
from sqlalchemy.orm import Session
from ..main import blacklist
from db import get_db


class LoginResource(Resource):
    def post(self):
        db: Session = next(get_db())
        data = request.json
        username = data.get('username')
        password = data.get('password')
        user = db.query(User).filter(User.username == username).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity={'id': user.id, 'username': user.username})
            refresh_token = create_refresh_token(identity={'id': user.id, 'username': user.username})
            return {'access_token': access_token, 'refresh_token': refresh_token}, 200
        return {'message': 'Invalid username or password'}, 401

class RefreshResource(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 200

class LogoutResource(Resource):
    @jwt_required()
    def post(self):
        jti = get_jwt_identity()['jti']
        blacklist.add(jti)
        return {'message': 'Logout successful'}, 200
