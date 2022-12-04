import pymongo
from bson.objectid import ObjectId
import os

class database:
    def __init__(self):
        mongoKey = os.getenv('MONGOKEY')
        mongoString = 'mongodb+srv://website_service:{}' \
            '@limelakeanalytics.eclfe.mongodb.net/' \
            'myFirstDatabase?retryWrites=true&w=majority' \
            .format(mongoKey)
        print(mongoString)
        self.client = pymongo.MongoClient(mongoString)

        self.db = self.client.limeLakeAnalytics
        self.posts = self.db.posts


    def get_posts(self):
        return self.posts.find()

    def get_post(self, id):
        return self.posts.find_one({"_id": ObjectId(id)})


