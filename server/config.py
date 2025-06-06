import os
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_cors import CORS  # Add CORS
from flask_restful import Api
from server.app import LoginResource, SignupResource

# Load environment variables from .env
load_dotenv()

# Use DATABASE_URL directly from .env (as provided by Render)
database_url = os.getenv("DATABASE_URL")
if not database_url:
    raise ValueError("DATABASE_URL is not set in your .env file. Please check your configuration.")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Enable CORS for all routes (allow frontend to access API)
CORS(app)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)

# Register API resources
api.add_resource(LoginResource, '/login')
api.add_resource(SignupResource, '/signup')
