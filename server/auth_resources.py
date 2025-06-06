from flask import request
from flask_restful import Resource
from server.models import Student, Instructor
from random import randint
import logging

logger = logging.getLogger(__name__)

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        user_type = data.get('userType')
        email = data.get('email')
        password = data.get('password')

        logger.info(f"Login attempt for userType: {user_type}, email: {email}")

        if user_type == 'student':
            user = Student.query.filter_by(email=email).first()
        else:
            user = Instructor.query.filter_by(email=email).first()

        if user and user.password_hash and user.check_password(password):
            logger.info(f"Login successful for user {email}")
            return {"id": user.id, "email": user.email, "name": user.name, "userType": user_type}, 200

        logger.warning(f"Login failed for user {email}")
        return {"error": "Invalid credentials"}, 401

class SignupResource(Resource):
    def post(self):
        data = request.get_json()
        user_type = data.get('userType')
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        logger.info(f"Signup attempt for userType: {user_type}, email: {email}")

        if user_type == 'student':
            if Student.query.filter_by(email=email).first():
                logger.warning(f"Signup failed: Email already exists for {email}")
                return {"error": "Email already exists"}, 400
            new_user = Student(name=name, email=email)
            new_user.set_password(password)
        else:
            if Instructor.query.filter_by(email=email).first():
                logger.warning(f"Signup failed: Email already exists for {email}")
                return {"error": "Email already exists"}, 400
            new_user = Instructor(name=name, email=email, department_id=randint(1, 18))
            new_user.set_password(password)

        from server.config import db
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"Signup successful for user {email}")
        return {"id": new_user.id, "email": new_user.email, "name": new_user.name, "userType": user_type}, 201
