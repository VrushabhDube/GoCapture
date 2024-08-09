from flask import request,abort
from flask_restful import Resource
from app.models import User, Task
from app.db import get_db
from sqlalchemy.orm import Session
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserResource(Resource):
        
    @jwt_required()
    def get(self, user_id=None):
        db: Session = next(get_db())
        if user_id is None:
            users = db.query(User).all()
            return [
                {
                    "id": user.id,
                    "username": user.username
                }
                for user in users
            ]
        else:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                return {"message": "User not found"}, 404
            return {
                "id": user.id,
                "username": user.username
            }
    @jwt_required()
    def post(self):
        db: Session = next(get_db())
        data = request.json
        new_user = User(
            username=data['username'],
            password=data['password']
        )
        db.add(new_user)
        db.commit()
        return {
            "id": new_user.id,
            "username": new_user.username
        }, 201
    
    @jwt_required()
    def put(self, user_id):
        db: Session = next(get_db())
        data = request.json
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"message": "User not found"}, 404
        user.username = data.get('username', user.username)
        if 'password' in data:
            user.password = user.hash_password(data['password'])
        db.commit()
        return {
            "id": user.id,
            "username": user.username
        }

    @jwt_required()
    def delete(self, user_id):
        db: Session = next(get_db())
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {"message": "User not found"}, 404
        db.delete(user)
        db.commit()
        return {"message": "User deleted"}, 204

class TaskResource(Resource):
    @jwt_required()
    def get(self, task_id=None):
        db: Session = next(get_db())
        user_id = request.args.get('user_id')
        if task_id is None:
            if not user_id:
                abort(400, description="User ID required")
            tasks = db.query(Task).filter(Task.user_id == user_id).all()
            return [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "status": task.status,
                    "priority": task.priority,
                    "due_at": task.due_at,
                    "created_at": task.created_at,
                    "updated_at": task.updated_at,
                    "user_id": task.user_id
                }
                for task in tasks
            ]
        else:
            task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
            if not task:
                return {"message": "Task not found"}, 404
            return {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_at": task.due_at,
                "created_at": task.created_at,
                "updated_at": task.updated_at,
                "user_id": task.user_id
            }

    @jwt_required()
    def post(self):
        db: Session = next(get_db())
        data = request.json
        user_id = data.get('user_id')
        if not db.query(User).filter(User.id == user_id).first():
            return {"message": "User not found"}, 404
        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            status=data['status'],
            priority=data['priority'],
            due_at=data.get('due_at'),
            user_id=user_id
        )
        db.add(new_task)
        db.commit()
        return {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "status": new_task.status,
            "priority": new_task.priority,
            "due_at": new_task.due_at,
            "created_at": new_task.created_at,
            "updated_at": new_task.updated_at,
            "user_id": new_task.user_id
        }, 201

    @jwt_required()
    def put(self, task_id):
        db: Session = next(get_db())
        data = request.json
        user_id = data.get('user_id')
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if not task:
            return {"message": "Task not found or not owned by user"}, 404
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.priority = data.get('priority', task.priority)
        task.due_at = data.get('due_at', task.due_at)
        task.user_id = data.get('user_id', task.user_id)
        db.commit()
        return {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "due_at": task.due_at,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "user_id": task.user_id
        }
    
    @jwt_required()
    def delete(self, task_id):
        db: Session = next(get_db())
        user_id = request.args.get('user_id')
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if not task:
            return {"message": "Task not found or not owned by user"}, 404
        db.delete(task)
        db.commit()
        return {"message": "Task deleted"}, 204
