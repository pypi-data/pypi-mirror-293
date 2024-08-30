from pymongo import MongoClient
from typing import Dict, List

class MongoDBConnector:
    def __init__(self, settings):
        self.db_enabled = settings.database.get("db_enabled", True)
        if self.db_enabled:
            self.client = MongoClient(
                settings.database["host"],
                settings.database["port"],
                username=settings.database["username"],
                password=settings.database["password"]
            )
            self.db = self.client[settings.database["dbname"]]
        else:
            self.local_db: Dict[str, List[Dict]] = {}

    def get_collection(self, model_name: str):
        if self.db_enabled:
            return self.db[model_name.lower()]
        else:
            if model_name.lower() not in self.local_db:
                self.local_db[model_name.lower()] = []
            return self.local_db[model_name.lower()]

    def insert_one(self, collection, item: Dict):
        if self.db_enabled:
            result = collection.insert_one(item)
            return {"id": str(result.inserted_id)}
        else:
            item["_id"] = len(collection) + 1
            collection.append(item)
            return {"id": str(item["_id"])}

    def find(self, collection):
        if self.db_enabled:
            return list(collection.find())
        else:
            return collection

    def find_one(self, collection, query: Dict):
        if self.db_enabled:
            return collection.find_one(query)
        else:
            for item in collection:
                match = all(item.get(k) == v for k, v in query.items())
                if match:
                    return item
            return None

    def update_one(self, collection, query: Dict, update: Dict):
        if self.db_enabled:
            return collection.update_one(query, update)
        else:
            for index, item in enumerate(collection):
                match = all(item.get(k) == v for k, v in query.items())
                if match:
                    collection[index].update(update["$set"])
                    return {"matched_count": 1}
            return {"matched_count": 0}

    def delete_one(self, collection, query: Dict):
        if self.db_enabled:
            return collection.delete_one(query)
        else:
            for index, item in enumerate(collection):
                match = all(item.get(k) == v for k, v in query.items())
                if match:
                    del collection[index]
                    return {"deleted_count": 1}
            return {"deleted_count": 0}
