import pymongo


class Database(object):
    URI = ['localhost:27017']
    DATABASE = None

    @staticmethod
    def inti():
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client["current"]

    @staticmethod
    def insert(collection, data):
        return Database.DATABASE[collection].insert(data)

    @staticmethod
    def find(collection, query):
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection, query) -> dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def get_all(collection):
        return Database.DATABASE[collection].find()

    @staticmethod
    def update_one(collection, query, data):
        return Database.DATABASE[collection].update(query, data)

    @staticmethod
    def delete(collection, query):
        return Database.DATABASE[collection].remove(query)
