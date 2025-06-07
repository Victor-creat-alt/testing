import random
import logging
from flask_restful import Api, Resource
from flask import request, jsonify
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func
from random import randint
from server.config import app, db
from server.models import Student, Course, Instructor, Department, Enrollment

logger = logging.getLogger(__name__)

api = Api(app)
with app.app_context():
    db.create_all()

class StudentResource(Resource):
    def get(self, student_id=None):
        if student_id:
            student = db.session.get(Student, student_id)
            if student:
                return student.to_dict(), 200
            return {"error": "Student not found."}, 404
        students = [s.to_dict() for s in Student.query.all()]
        return students, 200

    def post(self):
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            return {"error": "Missing required fields"}, 400

        new_student = Student(name=data['name'], email=data['email'])
        new_student.set_password(data['password'])
        db.session.add(new_student)
        try:
            db.session.commit()
            return new_student.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Email already exists"}, 400

    def patch(self, student_id):
        student = db.session.get(Student, student_id)
        if not student:
            return {"error": "Student not found"}, 404

        data = request.get_json()
        if 'name' in data:
            student.name = data['name']
        if 'email' in data:
            student.email = data['email']
        if 'password' in data:
            try:
                password = data['password'].strip()
                student.set_password(password)
            except AssertionError as e:
                return {"error": str(e)}, 400

        db.session.commit()
        return student.to_dict(), 200

    def put(self, student_id):
        student = db.session.get(Student, student_id)
        if not student:
            return {"error": "Student not found"}, 404

        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            return {"error": "Missing required fields"}, 400

        student.name = data['name']
        student.email = data['email']
        student.set_password(data['password'])

        db.session.commit()
        return student.to_dict(), 200

    def delete(self, student_id):
        student = db.session.get(Student, student_id)
        if not student:
            return {"error": "Student not found"}, 404

        db.session.delete(student)
        db.session.commit()
        return '', 204

class CourseResource(Resource):
    def get(self, course_id=None):
        if course_id:
            course = db.session.get(Course, course_id)
            if course:
                return course.to_dict(), 200
            return {"error": "Course not found"}, 404
        courses = [c.to_dict() for c in Course.query.all()]
        return courses, 200

    def post(self):
        data = request.get_json()
        if not data or not all(k in data for k in ('title', 'description', 'duration', 'image_url', 'instructor_id')):
            return {"error": "Missing required fields"}, 400

        new_course = Course(
            title=data['title'],
            description=data['description'],
            duration=data['duration'],
            instructor_id=data['instructor_id'],
            image_url=data['image_url'],
        )
        db.session.add(new_course)
        try:
            db.session.commit()
            return new_course.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Integrity Error, check instructor_id or department_id"}, 400

    def patch(self, course_id):
        course = db.session.get(Course, course_id)
        if not course:
            return {"error": "Course not found"}, 404

        data = request.get_json()
        for field in ['title', 'description', 'duration', 'instructor_id', 'image_url', 'department_id']:
            if field in data:
                setattr(course, field, data[field])

        db.session.commit()
        return course.to_dict(), 200

    def put(self, course_id):
        course = db.session.get(Course, course_id)
        if not course:
            return {"error": "Course not found"}, 404

        data = request.get_json()
        if not data or not all(k in data for k in ('title', 'description', 'duration', 'image_url', 'instructor_id')):
            return {"error": "Missing required fields"}, 400

        course.title = data['title']
        course.description = data['description']
        course.duration = data['duration']
        course.instructor_id = data['instructor_id']
        course.image_url = data['image_url']

        db.session.commit()
        return course.to_dict(), 200

    def delete(self, course_id):
        course = db.session.get(Course, course_id)
        if not course:
            return {"error": "Course not found"}, 404

        db.session.delete(course)
        db.session.commit()
        return '', 204

class InstructorsResource(Resource):
    def get(self, instructor_id=None):
        if instructor_id:
            instructor = db.session.get(Instructor, instructor_id)
            if instructor:
                return instructor.to_dict(), 200
            return {"error": "Instructor not found"}, 404
        instructors = [i.to_dict() for i in Instructor.query.all()]
        return instructors, 200

    def post(self):
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'email', 'password')):
            return {"error": "Missing required fields"}, 400

        name = data['name']
        email = data['email']
        password = data['password']

        new_instructor = Instructor(
            name=name,
            email=email,
            department_id=random.randint(1, 18)
        )
        new_instructor.set_password(password)

        db.session.add(new_instructor)
        try:
            db.session.commit()
            return new_instructor.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {"error": "Email already exists"}, 400
        except Exception as e:
            db.session.rollback()
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500

    def put(self, instructor_id):
        data = request.get_json()
        instructor = db.session.get(Instructor, instructor_id)

        if not instructor:
            return {"error": "Instructor not found"}, 404

        instructor.name = data.get('name', instructor.name)
        instructor.email = data.get('email', instructor.email)
        if 'password' in data:
            instructor.set_password(data['password'])

        try:
            db.session.commit()
            return instructor.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def patch(self, instructor_id):
        data = request.get_json()
        instructor = db.session.get(Instructor, instructor_id)

        if not instructor:
            return {"error": "Instructor not found"}, 404

        if 'name' in data:
            instructor.name = data['name']
        if 'email' in data:
            instructor.email = data['email']
        if 'password' in data:
            instructor.set_password(data['password'])

        try:
            db.session.commit()
            return instructor.to_dict(), 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

    def delete(self, instructor_id):
        instructor = db.session.get(Instructor, instructor_id)

        if not instructor:
            return {"error": "Instructor not found"}, 404

        try:
            db.session.delete(instructor)
            db.session.commit()
            return {"message": "Instructor deleted"}, 200
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 500

class DepartmentResource(Resource):
    def get(self, department_id=None):
        if department_id:
            department = db.session.get(Department, department_id)
            if department:
                return department.to_dict(), 200
            return {"error": "Department not found"}, 404
        departments = [d.to_dict() for d in Department.query.all()]
        return departments, 200

    def post(self):
        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'location', 'head')):
            return {"error": "Missing required fields"}, 400

        new_department = Department(
            name=data['name'],
            location=data['location'],
            head=data['head']
        )
        db.session.add(new_department)
        db.session.commit()
        return new_department.to_dict(), 201

    def patch(self, department_id):
        department = db.session.get(Department, department_id)
        if not department:
            return {"error": "Department not found"}, 404

        data = request.get_json()
        for field in ['name', 'location', 'head']:
            if field in data:
                setattr(department, field, data[field])

        db.session.commit()
        return department.to_dict(), 200

    def put(self, department_id):
        department = db.session.get(Department, department_id)
        if not department:
            return {"error": "Department not found"}, 404

        data = request.get_json()
        if not data or not all(k in data for k in ('name', 'location', 'head')):
            return {"error": "Missing required fields"}, 400

        department.name = data['name']
        department.location = data['location']
        department.head = data['head']

        db.session.commit()
        return department.to_dict(), 200

    def delete(self, department_id):
        department = db.session.get(Department, department_id)
        if not department:
            return {"error": "Department not found"}, 404

        db.session.delete(department)
        db.session.commit()
        return '', 204

class EnrollmentResource(Resource):
    def get(self, enrollment_id=None):
        if enrollment_id:
            enrollment = db.session.get(Enrollment, enrollment_id)
            if enrollment:
                return enrollment.to_dict(), 200
            return {"error": "Enrollment not found"}, 404

        # Support filtering by studentId and courseId query parameters
        student_id = request.args.get('studentId', type=int)
        course_id = request.args.get('courseId', type=int)

        query = Enrollment.query
        if student_id is not None:
            query = query.filter_by(student_id=student_id)
        if course_id is not None:
            query = query.filter_by(course_id=course_id)

        enrollments = [e.to_dict() for e in query.all()]
        return enrollments, 200

    def post(self):
        data = request.get_json()
        # Accept camelCase keys from frontend
        if not data or not all(k in data for k in ('studentId', 'courseId')):
            return {"error": "Missing required fields."}, 400

        student_id = data['studentId']
        course_id = data['courseId']

        new_enrollment = Enrollment(
            student_id=student_id,
            course_id=course_id,
        )
        db.session.add(new_enrollment)
        try:
            db.session.commit()
            self.update_student_grade(student_id)
            return new_enrollment.to_dict(), 201
        except Exception as e:
            db.session.rollback()
            return {"error": str(e)}, 400

    def patch(self, enrollment_id):
        enrollment = db.session.get(Enrollment, enrollment_id)
        if not enrollment:
            return {'error': "Enrollment not found"}, 404

        data = request.get_json()
        for field in ['student_id', 'course_id']:
            if field in data:
                setattr(enrollment, field, data[field])

        db.session.commit()
        self.update_student_grade(enrollment.student_id)
        return enrollment.to_dict(), 200

    def put(self, enrollment_id):
        enrollment = db.session.get(Enrollment, enrollment_id)
        if not enrollment:
            return {'error': "Enrollment not found"}, 404

        data = request.get_json()
        if not data or not all(k in data for k in ('student_id', 'course_id')):
            return {"error": "Missing required fields."}, 400

        enrollment.student_id = data['student_id']
        enrollment.course_id = data['course_id']

        db.session.commit()
        self.update_student_grade(enrollment.student_id)
        return enrollment.to_dict(), 200

    def delete(self, enrollment_id):
        enrollment = db.session.get(Enrollment, enrollment_id)
        if not enrollment:
            return {"error": "Enrollment not found"}, 404

        student_id = enrollment.student_id
        db.session.delete(enrollment)
        db.session.commit()
        self.update_student_grade(student_id)
        return '', 204

    def update_student_grade(self, student_id):
        enrollment_count = Enrollment.query.filter_by(student_id=student_id).count()
        grade = 'Low'
        if enrollment_count >= 3:
            grade = 'Average'
        if enrollment_count >= 5:
            grade = 'Excellent'

        enrollments = Enrollment.query.filter_by(student_id=student_id).all()
        for enrollment in enrollments:
            enrollment.grade = grade
        db.session.commit()

class StudentEnrollmentCountResource(Resource):
    def get(self):
        enrollment_counts = db.session.query(
            Student.name,
            func.count(Enrollment.id).label('enrollment_count')
        ).join(Enrollment).group_by(Student.id).all()
        return [{'name': name, 'enrollmentCount': count} for name, count in enrollment_counts], 200

class EnrolledStudentsResource(Resource):
    def get(self, student_id=None):
        if student_id:
            enrollments = Enrollment.query.filter_by(student_id=student_id).all()
            if not enrollments:
                return {"error": "Student has no enrollments"}, 404
            result = [enrollment.to_dict() for enrollment in enrollments]
            return result, 200

        enrollments = Enrollment.query.all()
        return [enrollment.to_dict() for enrollment in enrollments], 200

class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            logger.warning("Login failed: No data provided")
            return {"error": "No data provided"}, 400

        user_type = data.get('userType')
        email = data.get('email')
        password = data.get('password')

        if user_type not in ['student', 'instructor']:
            logger.warning(f"Login failed: Invalid userType {user_type}")
            return {"error": "Invalid userType"}, 400

        if not email or not password:
            logger.warning("Login failed: Missing email or password")
            return {"error": "Missing email or password"}, 400

        email = email.lower().strip()
        password = password.strip()
        logger.info(f"Login attempt for userType: {user_type}, email: {email}")

        if user_type == 'student':
            user = Student.query.filter(func.lower(Student.email) == email).first()
        else:
            user = Instructor.query.filter(func.lower(Instructor.email) == email).first()

        if user is None:
            logger.warning(f"Login failed: User not found for email {email}")
            return {"error": "Invalid credentials"}, 401

        if not user.password_hash:
            logger.warning(f"Login failed: No password set for user {email}")
            return {"error": "Invalid credentials"}, 401

        logger.debug(f"Password hash for user {email}: {user.password_hash}")

        # Additional detailed logging for password check
        try:
            password_check_result = user.check_password(password)
            logger.debug(f"Password check result for user {email}: {password_check_result}")
        except Exception as e:
            logger.error(f"Exception during password check for user {email}: {str(e)}")
            return {"error": "Invalid credentials"}, 401

        if password_check_result:
            logger.info(f"Login successful for user {email}")
            return {"id": user.id, "email": user.email, "name": user.name, "userType": user_type}, 200
        else:
            logger.warning(f"Login failed: Incorrect password for user {email}")
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
            try:
                password = password.strip()
                new_user.set_password(password)
            except AssertionError as e:
                return {"error": str(e)}, 400
        else:
            if Instructor.query.filter_by(email=email).first():
                logger.warning(f"Signup failed: Email already exists for {email}")
                return {"error": "Email already exists"}, 400
            new_user = Instructor(name=name, email=email, department_id=randint(1, 18))
            try:
                password = password.strip()
                new_user.set_password(password)
            except AssertionError as e:
                return {"error": str(e)}, 400

        from server.config import db
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"Signup successful for user {email}")
        return {"id": new_user.id, "email": new_user.email, "name": new_user.name, "userType": user_type}, 201

class ResetPasswordResource(Resource):
    def post(self):
        data = request.get_json()
        new_password = data.get('new_password')
        email = data.get('email')

        if not new_password or not email:
            return {"error": "Email and new_password are required."}, 400

        # Validate password length and digit presence
        if len(new_password) < 8:
            return {"error": "Password must be at least 8 characters long."}, 400
        if not any(char.isdigit() for char in new_password):
            return {"error": "Password must contain at least one digit."}, 400

        # Find user by email in Student or Instructor tables
        user = Student.query.filter(func.lower(Student.email) == email.lower()).first()
        if not user:
            user = Instructor.query.filter(func.lower(Instructor.email) == email.lower()).first()
        if not user:
            return {"error": "User not found."}, 404

        try:
            user.set_password(new_password)
            db.session.commit()
            return {"message": "Password reset successful."}, 200
        except Exception as e:
            return {"error": f"Failed to reset password: {str(e)}"}, 500


# Register API resources
api.add_resource(LoginResource, '/login')
api.add_resource(SignupResource, '/signup')
api.add_resource(ResetPasswordResource, '/reset-password')
api.add_resource(StudentResource, '/students', '/students/<int:student_id>')
api.add_resource(CourseResource, '/courses', '/courses/<int:course_id>')
api.add_resource(InstructorsResource, '/instructors', '/instructors/<int:instructor_id>')
api.add_resource(DepartmentResource, '/departments', '/departments/<int:department_id>')
api.add_resource(EnrollmentResource, '/enrollments', '/enrollments/<int:enrollment_id>')
api.add_resource(StudentEnrollmentCountResource, '/student_enrollment_counts')
api.add_resource(EnrolledStudentsResource, '/enrolled_students', '/enrolled_students/<int:student_id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
