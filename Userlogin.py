from database.db import Clients

class UserLogin():
    def __init__(self, user_id, nickname):
        self.id = user_id
        self.nickname = nickname

    @staticmethod
    def fromDB(user_id, session):
        user = session.query(Clients).get(user_id)
        if user:
            return UserLogin(user.idclients, user.nickname)
        return None

    def is_active(self):
        return True

    def is_authenticated(self):
        return self.is_active()

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)
