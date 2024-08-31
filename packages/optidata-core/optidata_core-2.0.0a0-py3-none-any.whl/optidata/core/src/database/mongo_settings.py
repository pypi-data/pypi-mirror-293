# MongoDB Configuration
import os

MONGO_BATCH_SIZE = 100000
MONGO_DB_HOST = os.environ.get("MONGO_HOST")
MONGO_DB_PORT = int(os.environ.get("MONGO_PORT"))
MONGO_DB_NAME = os.environ.get("MONGO_DBNAME")
MONGO_DB_URI = f'mongodb://{MONGO_DB_HOST}:{MONGO_DB_PORT}/{MONGO_DB_NAME}'
MONGO_DB_USER = os.environ.get("MONGO_USR")
MONGO_DB_PWD = os.environ.get("MONGO_PWD")
