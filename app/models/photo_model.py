import mongoengine


class Photo(mongoengine.Document):
    author = mongoengine.StringField()
    url = mongoengine.StringField()
    active = mongoengine.BooleanField()
    timestamp = mongoengine.DateTimeField()
    likes = mongoengine.IntField()
