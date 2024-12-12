from dotenv import load_dotenv

load_dotenv()

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False

    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {}


class LocalDevelopmentConfig(Config):
    DEBUG = True

    # SQLite database
    SQLITE_DB_DIR = os.path.join(basedir)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "database.sqlite3")
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SCHEDULER_JOBSTORES = {"default": {"type": "sqlalchemy", "url": SQLALCHEMY_DATABASE_URI}}
    SCHEDULER_API_ENABLED = True
