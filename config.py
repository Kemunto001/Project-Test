import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://username:password@localhost/db_name')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
    AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
    AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
