from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from app.resources import UserResource, TaskResource
from app.db import engine
from app.models import Base
from app.auth import LoginResource,LogoutResource

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'dfgfgfg8487g8gdfgdf8gd8gd'  
jwt = JWTManager(app)

api = Api(app)

Base.metadata.create_all(engine)

# Token blacklist
blacklist = set()

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in blacklist

@jwt.additional_claims_loader
def add_claims_to_access_token(identity):
    return {'jti': identity.get('id')}

api.add_resource(UserResource, '/users', '/users/<int:user_id>')
api.add_resource(TaskResource, '/tasks', '/tasks/<int:task_id>')
api.add_resource(LoginResource, '/login')
api.add_resource(LogoutResource, '/logout')

if __name__ == '__main__':
    app.run(debug=True)