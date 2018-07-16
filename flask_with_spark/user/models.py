from application import db
from utilities.common import utc_now_ts as now


class User(db.Document):
    username = db.StringField(db_field="u", required=True)
    password = db.StringField(db_field="p", required=True)
    email = db.EmailField(db_field="e", required=True, unique=True)
    created = db.IntField(db_filed="c", default=now())
    meta = {'indexes': ['username', 'email', '-created']}
