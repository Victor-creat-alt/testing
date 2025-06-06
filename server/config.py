import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Load environment variables from .env
load_dotenv()

user = os.getenv("PG_USERNAME")
password = os.getenv("PG_PASSWORD")
host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")
database = os.getenv("PG_DATABASE")

if not all([user, password, host, port, database]):
    raise ValueError("Missing one or more required environment variables. Check your .env file.")

# Flask app setup
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{user}:{password}@{host}:{port}/{database}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)