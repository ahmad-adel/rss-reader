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

    def insert(self, post_pk: int, data: dict) -> None:
        obj = {
            "pk": str(post_pk),
            "data": data,
        }
        self.collection.insert_one(obj)

    def fetch(self, post_pk: int) -> dict:
        query = {"pk": str(post_pk)}
        data_obj = self.collection.find(query)
        
        data_list = [document["data"] for document in data_obj]

        if len(data_list) > 0:
            return data_list[0]
        else:
            return {}

    def update_one(self, post_pk: int, data: dict) -> None:
        query = {"pk": str(post_pk)}
        self.collection.update_one(query, {"$set":{"data": data}})

    def bulk_delete(self, post_pk_list: list[int]) -> None:
        post_pk_strs = [str(pk) for pk in post_pk_list]
        query = {'pk':{'$in': post_pk_strs}}
        self.collection.deleteMany(query)


RSSPostManagerInstance = RSSPostManager()
