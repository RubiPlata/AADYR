from models.user import User
from extensions import db, bcrypt


class AuthService:

    # =========================
    # REGISTER
    # =========================
    @staticmethod
    def register(username, email, password):
        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            return None

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        user = User(
            username=username,
            email=email,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        return user

    # =========================
    # LOGIN
    # =========================
    @staticmethod
    def login(username, password):
        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user

        return None

    # =========================
    # GET ALL USERS
    # =========================
    @staticmethod
    def get_all_users():
        return User.query.all()

    # =========================
    # FIND BY ID
    # =========================
    @staticmethod
    def find_by_id(user_id):
        return User.query.get(user_id)

    # =========================
    # UPDATE USER
    # =========================
    @staticmethod
    def update_user(user_id, username=None, email=None, password=None):
        user = User.query.get(user_id)

        if not user:
            return None

        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = bcrypt.generate_password_hash(password).decode("utf-8")

        db.session.commit()
        return user

    # =========================
    # DELETE USER
    # =========================
    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)

        if not user:
            return False

        db.session.delete(user)
        db.session.commit()

        return True