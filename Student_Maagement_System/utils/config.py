import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# Load environment variables from .env file
load_dotenv()

# JWT and database configuration variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# MongoDB configuration
mongodb_link = os.getenv("MONGODB_LINK")
if not mongodb_link:
    raise ValueError("MONGODB_LINK environment variable not set.")

# Set up MongoDB connection
uri = mongodb_link
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.student_management_db

# Collections for students and admins
collection = db["student_data"]
admin_collection = db["admin_data"]
