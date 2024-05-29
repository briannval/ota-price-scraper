import os

from dotenv import load_dotenv
from pymongo import MongoClient

from .ota import Ota


class OtaMongo(Ota):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.desc = "OTA Price Scraper For MongoDB Use"
        self.res = {}
        self.client = None
        self.db = None
        self.hotels = None
        self.__connect_to_mongodb()

    def __connect_to_mongodb(self):
        try:
            self.client = MongoClient(os.getenv("MONGO_URI"))
        except Exception as e:
            print(f"Error: {e}")
        self.db = self.client[os.getenv("MONGO_DATABASE")]
        self.hotels = self.db[os.getenv("MONGO_COLLECTION")]

    def __transpose_results(self):
        self.res = [
            {k: v[i] for k, v in self.scraping_results.items()}
            for i in range(len(self.scraping_results["Hotel Name"]))
        ]

    def __upload_to_mongodb(self):
        self.hotels.insert_many(self.res)
        print("Succesfully inserted to MongoDB")

    def finish(self):
        """
        Transform scraping results to array of dicts
        """
        self.__transpose_results()
        self.__upload_to_mongodb()
