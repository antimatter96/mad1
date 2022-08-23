import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config():
  DEBUG = False


class LocalDevConfig(Config):
  DEBUG = True

  SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "testdb.sqlite3")


class ProdConfig(Config):
  SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
  SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "prod.sqlite3")
