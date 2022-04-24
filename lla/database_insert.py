from database import database
from bson.objectid import ObjectId

db = database()

data = db.get_post(ObjectId("625f6c193188f273a771e86e"))

print(data['post_text'])