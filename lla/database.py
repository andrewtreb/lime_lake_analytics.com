import pymongo
from bson.objectid import ObjectId
import os
from datetime import datetime, timedelta
import pandas as pd

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
        self.weatherData = self.db.weatherData


    def get_posts(self):
        return self.posts.find()

    def get_post(self, id):
        return self.posts.find_one({"_id": ObjectId(id)})

    def get_allWeatherData(self):
        #lastHour = datetime.now() - timedelta(hours = 1)
        #criteria = { 'data_time': {'$gt': lastHour}}

        cursor = self.weatherData.find()
        df = pd.DataFrame(list(cursor))

        #print(df.shape)

        return df


