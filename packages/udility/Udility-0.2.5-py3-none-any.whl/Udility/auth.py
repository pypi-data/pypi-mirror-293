# auth.py

import os
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash

# MongoDB Atlas connection string (Replace with your actual connection string)
MONGO_URI = os.getenv("MONGO_URI", "your_mongodb_atlas_connection_string")
client = MongoClient(MONGO_URI)
db = client["UdilityDB"]
users_collection = db["users"]

def register_user(email, password, api_key):
    """Register a new user and store hashed password and OpenRouter API key."""
    if users_collection.find_one({"email": email}):
        return "User already exists."

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    
    users_collection.insert_one({
        "email": email,
        "password": hashed_password,
        "api_key": api_key
    })
    return "User registered successfully."

def login_user(email, password):
    """Authenticate a user and retrieve their OpenRouter API key."""
    user = users_collection.find_one({"email": email})
    if not user:
        return None, "User not found."
    
    if check_password_hash(user["password"], password):
        return user["api_key"], "Login successful."
    else:
        return None, "Incorrect password."

def authenticate():
    """Prompt user for email and password to authenticate and store API key."""
    email = input("Enter your email: ")
    password = input("Enter your password: ")

    api_key, message = login_user(email, password)
    if not api_key:
        print(message)
        api_key = os.environ.get('DEFAULT_API_KEY')  # Use the default API key stored in environment variables
        register_message = register_user(email, password, api_key)
        print(register_message)
    else:
        print(message)

    os.environ["OPENROUTER_API_KEY"] = api_key
