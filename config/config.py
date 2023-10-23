import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f'mysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@db/{os.getenv("DB_NAME")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f'mysql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@db_test/{os.getenv("TEST_DB_NAME")}'