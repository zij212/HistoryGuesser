import pymongo
import os
import uuid


class Database:
    conn_str = f"mongodb+srv://{os.environ['DBUSER']}:{os.environ['DBPASS']}@{os.environ['URI']}?retryWrites=true&w=majority"
    DATABASE = None

    @staticmethod
    def initialize():
        client = pymongo.MongoClient(Database.conn_str)
        Database.db = client['games']

    @staticmethod
    def find_top_n(collection, field, n, order=-1):
        data = Database.db[collection].find({},{'_id': False}, sort=[(field, order)]).limit(n)
        return [*data]

    @staticmethod
    def insert(collection, data):
        Database.db[collection].insert(data)


class Highscore:
    def __init__(self, username, score, topic, _id=None):
        self.username = username
        self.score = score
        self.topic = topic
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self):
        return {
            "username": self.username,
            "score": self.score,
            "topic": self.topic,
            "_id": self._id,
        }

    def save_to_mongo(self):
        Database.insert(collection='highscores', data=self.json())
