from flask_login import UserMixin
from flask import g

class UserLogin(UserMixin):
    def fromDB(self, user_id, db, table):
        self.user = db.get_user(user_id, table)
        return self
    
    def create(self, user):
        self.user = user
        return self

    def get_id(self):
        return str(self.user.id)