# config.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from sqlalchemy import MetaData

# Flask App Configuration
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Metadata configuration for migrations
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Database and Extensions
db = SQLAlchemy(app, metadata=metadata) #Initialize the database with the app
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)

# Import models to ensure they are registered with SQLAlchemy
from models import Student, Course, Instructor, Department, Enrollment