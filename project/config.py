import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config():
  DEBUG = False
  SQLITE_DB_DIR = None
  SQLALCHEMY_DATABASE_URI = None
  SQLALCHEMY_TRACK_MODIFICATIONS = False

class NonProdConfig(Config):
  DEBUG = True
  SECURITY_REGISTERABLE = True
  SECURITY_CONFIRMABLE = False
  SECURITY_SEND_REGISTER_EMAIL = False
  SECURITY_UNAUTHORIZED_VIEW = None

class LocalDevelopmentConfig(NonProdConfig):
  SQLITE_DB_DIR = os.path.join(basedir, "./db_directory")
  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "local.sqlite3")
  SECRET_KEY = "ash ah secet"
  SECURITY_PASSWORD_HASH = "bcrypt"
  SECURITY_PASSWORD_SALT = "really super secret"

class TestingConfig(NonProdConfig):
  SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
  SECRET_KEY = "ash ah secet"
  SECURITY_PASSWORD_HASH = "bcrypt"
  SECURITY_PASSWORD_SALT = "really super secret"
  WTF_CSRF_ENABLED = False
