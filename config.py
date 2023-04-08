import os
import sys

from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class Config:
    """Set Flask configuration vars from .env file."""

    APP_NAME = "FLASK_MONGODB_BACKEND"

    # MONGO database
    MONGODB_HOST = os.getenv("DB_HOST")
    MONGODB_DB = os.getenv("DB_NAME")
    MONGODB_PORT = int(os.getenv("DB_PORT", default=27017))
    MONGODB_USERNAME = os.getenv("DB_USER")
    MONGODB_PASSWORD = os.getenv("DB_PASSWORD")

    # REDIS
    REDIS_SERVER = os.getenv("REDIS_SERVER")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")

    # General
    DEBUG = False
    DEVELOPMENT = False
    SECRET_KEY = os.getenv("SECRET_KEY", default="SECRET")
    FLASK_RUN_PORT = 6000
    TESTING = False
    LOG_HEADER = f"error_log[{APP_NAME}]"

    JWT_ALGORITHMS = "HS256"

    # MAIL CONFIGURATION
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_SERVER_PORT = int(os.getenv("MAIL_SERVER_PORT", default=587))
    DEFAULT_MAIL_SENDER_ADDRESS = os.getenv("DEFAULT_MAIL_SENDER_ADDRESS")
    DEFAULT_MAIL_SENDER_PASSWORD = os.getenv("DEFAULT_MAIL_SENDER_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER")
    ADMIN_MAIL_ADDRESSES = os.getenv("ADMIN_MAIL_ADDRESSES", default="").split("|")

    @property
    def MONGODB_SETTINGS(self):  # noqa
        return [
            {
                "db": self.MONGODB_DB,
                "host": self.MONGODB_HOST,
                "port": self.MONGODB_PORT,
                "username": self.MONGODB_USERNAME,
                "password": self.MONGODB_PASSWORD,
            }
        ]


class DevelopmentConfig(Config):
    DEBUG = True
    DEVELOPMENT = True
    SQL_DB_HOST = os.getenv("DB_HOST", default="localhost")
    LOG_BACKTRACE = True
    LOG_LEVEL = "DEBUG"


class ProductionConfig(Config):
    DEBUG = False
    DEVELOPMENT = False
    SQL_DB_HOST = os.getenv("DB_HOST")
    LOG_BACKTRACE = False
    LOG_LEVEL = "INFO"


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DEVELOPMENT = True
    LOG_BACKTRACE = True
    LOG_LEVEL = "DEBUG"

    @property
    def MONGODB_SETTINGS(self):
        return []
