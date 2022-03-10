import os
basedir = os.path.abspath(os.path.dirname(__file__))

from decouple import config
from datetime import timedelta

class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = config('SECRET_KEY', "SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=30)
    JWT_SECRET_KEY=config('JWT_SECRET_KEY')
    UPLOAD_FOLDER="uploads/"
    ALLOWED_EXTENSIONS = set(['pdf'])


class ProductionConfig(Config):
    DEVELOPMENT = False
    TESTING = False
    DEBUG = False
    UPLOAD_FOLDER="uploads/"
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URI', "DATABASE_URI")


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://test_user:test_pass@localhost:5432/test_db'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = config('DATABASE_URI', "DATABASE_URI")