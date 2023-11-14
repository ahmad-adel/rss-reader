import pymongo
from pymongo import MongoClient
from pymongo.collection import Collection
from django.conf import settings


class RSSPostManager:
    def __init__(self) -> None:
        self.collection_name = "rss_post"
        self.client: MongoClient = MongoClient(
            settings.MONGO_DB_HOST,
            settings.MONGO_DB_PORT,
            username=settings.MONGO_DB_USERNAME,
            password=settings.MONGO_DB_PASSWORD,
        )
        self.collection = self._connect()

    def _connect(self) -> Collection:
        db = self.client[settings.MONGO_DB_NAME]
        collection = db[self.collection_name]
        return collection

    def insert(self, guid: str, data: dict):
        obj = {
            "guid": guid,
            "data": data,
        }
        self.collection.insert_one(obj)

    def fetch(self, guid: str) -> dict:
        query = {"guid": guid}
        data_obj = self.collection.find(query)
        
        data_list = [document["data"] for document in data_obj]

        if len(data_list) > 0:
            return data_list[0]
        else:
            return {}

    def bulk_delete(self, guid_list: list[str]) -> None:
        query = {'guid':{'$in': guid_list}}
        self.collection.deleteMany(query)


RSSPostManagerInstance = RSSPostManager()
