# Import necessary libraries and modules
from server.config import db  # Import database
from sqlalchemy.orm import validates  # Import validation helper for fields
from sqlalchemy_serializer import SerializerMixin  # Import serializer for JSON conversion
from sqlalchemy.ext.associationproxy import association_proxy  # Association Proxy for relationships
from werkzeug.security import generate_password_hash, check_password_hash  # Import password hashing tools

# Define the Student model
class Student(db.Model, SerializerMixin):
    __tablename__ = 'students'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String, nullable=False)  # Non-nullable name field
    email = db.Column(db.String, unique=True, nullable=False)  # Unique and non-nullable email field
    password_hash = db.Column(db.String, nullable=False)  # Hashed password field (non-nullable)
    enrollments = db.relationship(
        "Enrollment", back_populates="student", cascade='all, delete-orphan', lazy=True
    )  # Relationship to Enrollment model, with cascading delete
    courses = association_proxy('enrollments', 'course')  # Proxy to access courses via enrollments
    serialize_rules = ('-password_hash', '-enrollments.student')  # Exclude sensitive data from serialization

    # Set hashed password
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    # Check if provided password matches the stored hash
    def check_password(self, password):
        try:
            return check_password_hash(self.password_hash, password)
        except ValueError:
            return False

    # Validate email format during assignment
    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Invalid email format"  # Ensure email contains '@'
        return email

    # Validate and hash password during assignment
    def set_password(self, password):
        assert len(password) >= 8, "Password must be at least 8 characters long."
        assert any(char.isdigit() for char in password), "Password must contain at least one number."
        self.password_hash = generate_password_hash(password)

# Define the Course model
class Course(db.Model, SerializerMixin):
    __tablename__ = 'courses'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    title = db.Column(db.String, nullable=False)  # Course title (non-nullable)
    description = db.Column(db.String, nullable=False)  # Course description (non-nullable)
    duration = db.Column(db.String, nullable=False)  # Course duration (non-nullable)
    image_url = db.Column(db.String(128))  # Optional image URL for the course
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id', ondelete='SET NULL'))  # Foreign key to instructor
    instructor = db.relationship("Instructor", back_populates="courses", lazy=True)  # Relationship with Instructor model
    students = association_proxy('enrollments', 'student')  # Proxy to access students via enrollments
    serialize_rules = ('-students.courses', '-instructor.courses')  # Exclude certain fields from serialization

# Define the Instructor model
class Instructor(db.Model, SerializerMixin):
    __tablename__ = 'instructors'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String, nullable=False)  # Instructor name (non-nullable)
    email = db.Column(db.String, unique=True, nullable=False)  # Unique and non-nullable email field
    password_hash = db.Column(db.String, nullable=False)  # Hashed password field (non-nullable)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))  # Foreign key to Department model
    courses = db.relationship("Course", back_populates="instructor", lazy=True)  # Relationship with Course model
    department = db.relationship("Department", back_populates="instructors", lazy=True)  # Relationship with Department model
    serialize_rules = ('-password_hash', '-courses.instructor', '-department.instructors')  # Exclude sensitive data

    # Define methods for password management (same as Student model)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        try:
            return check_password_hash(self.password_hash, password)
        except ValueError:
            return False

    @validates('email')
    def validate_email(self, key, email):
        assert '@' in email, "Invalid email format"
        return email

    def set_password(self, password):
        assert len(password) >= 8, "Password must be at least 8 characters long."
        assert any(char.isdigit() for char in password), "Password must contain at least one digit."
        self.password_hash = generate_password_hash(password)

# Define the Department model
class Department(db.Model, SerializerMixin):
    __tablename__ = 'departments'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    name = db.Column(db.String, nullable=False)  # Department name (non-nullable)
    location = db.Column(db.String, nullable=False)  # Department location (non-nullable)
    head = db.Column(db.String, nullable=False)  # Name of the department head (non-nullable)
    instructors = db.relationship("Instructor", back_populates="department", lazy=True)  # Relationship to Instructors
    serialize_rules = ('-instructors.department',)  # Exclude related instructors' departments from serialization

# Define the Enrollment model
class Enrollment(db.Model, SerializerMixin):
    __tablename__ = 'enrollments'  # Table name in the database
    id = db.Column(db.Integer, primary_key=True)  # Primary key column
    student_id = db.Column(
        db.Integer, db.ForeignKey('students.id', ondelete='CASCADE'), nullable=False
    )  # Foreign key linking to a Student; deletes if Student is deleted
    course_id = db.Column(
        db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False
    )  # Foreign key linking to a Course; deletes if Course is deleted
    grade = db.Column(db.String, default='Low')  # Optional grade, defaults to 'Low'
    student = db.relationship("Student", back_populates="enrollments", lazy=True)  # Relationship with Student model
    course = db.relationship("Course", lazy=True)  # Relationship with Course model
    serialize_rules = ('-student.enrollments', '-course.students')  # Exclude nested data from serialization
