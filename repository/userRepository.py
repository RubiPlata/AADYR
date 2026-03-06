from models.user import User
from extensions import db


class UserRepository:

    @staticmethod
    def get_all():
        return User.query.all()

    @staticmethod
    def get_by_username(username):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def find_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def create(username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def update(user, username=None, email=None, password=None):
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.set_password(password)

        db.session.commit()
        return user

    @staticmethod
    def delete(user):
        db.session.delete(user)
        db.session.commit()