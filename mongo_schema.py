from mongoengine import *
from settings import *

connect(db=MONGO_DB_NAME, host=MONGO_HOST_NAME, port=MONGO_HOST_PORT)

class TextDocument(Document):
    link = StringField()
    tag = StringField()
    message = StringField()
    title = StringField()