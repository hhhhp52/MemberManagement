import hashlib
import constants
from datetime import datetime
from dao import user


class AccountManager:
    def __init__(self, username: str = None, password: str = None):
        self.username = username
        self.password = password
        if password:
            self.hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        else:
            self.hashed_password = None

    def check_account(self):
        return user.account_exist_or_not(self.username)

    def create_account(self):
        return user.add_account(self.username, self.hashed_password)

    def check_failed_attempts(self):
        attempts, last_attempt_time = user.get_failed_attempts(self.username)
        if attempts:
            if attempts >= constants.MAX_FAILED_ATTEMPTS:
                if datetime.now() - datetime.fromisoformat(last_attempt_time) < constants.COOLDOWN_PERIOD:
                    return False
        return True

    def check_user_password(self):
        password = user.get_password_by_username(self.username)

        if password:
            if password != str(self.hashed_password):
                user.upsert_failed_attempts_db(self.username)
                return False
            else:
                user.delete_failed_attempts(self.username)
                return True
        else:
            user.upsert_failed_attempts_db(self.username)
            return False
