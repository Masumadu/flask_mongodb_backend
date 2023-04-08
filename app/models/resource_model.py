from datetime import datetime

from app import me


class ResourceModel(me.Document):
    title: str
    content: str

    meta = {"collection": "resource"}
    title = me.StringField()
    content = me.StringField()
    created = me.DateTimeField(default=datetime.now)
    modified = me.DateTimeField(default=datetime.now)
