from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME

_client = None
_db = None


def get_client():
    global _client
    if _client is None:
        _client = MongoClient(MONGO_URI)
    return _client


def get_database():
    global _db
    if _db is None:
        _db = get_client()[MONGO_DB_NAME]
    return _db


def get_collection(name):
    return get_database()[name]


def close_connection():
    global _client, _db
    if _client:
        _client.close()
        _client = None
        _db = None
