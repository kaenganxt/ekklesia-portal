from ekklesia_portal.database.datamodel import User
from ekklesia_portal.lib.password import password_context


class UserNotFound(ValueError):
    pass


class Login:
    def __init__(self, request=None, username=None, password=None):
        self.request = request
        self.username = username
        self.password = password
        self.user = None

    def find_user(self):
        if self.username is None or self.password is None:
            raise ValueError("username and/or password cannot be None")

        user = self.request.q(User).filter_by(name=self.username).scalar()
        if user is None:
            raise UserNotFound()

        self.user = user

    def verify_password(self, insecure_empty_password_ok):
        if self.user is None:
            raise ValueError("user is not set!")
        if insecure_empty_password_ok and self.password == '':
            return True
        if self.user.password is None:
            return False

        return password_context.verify(self.password, self.user.password.hashed_password)
