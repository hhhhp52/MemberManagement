from flask import jsonify
import re

from model import AccountManager

# Password validation regex pattern
password_pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,32}$')


def create_account_impl(username, password):
    if not username or not password:
        return False, dict(
            reason="Username and password are required",
            status_code=400
        )

    if len(username) < 3 or len(username) > 32:
        return False, dict(
            reason="Username must be between 3 and 32 characters",
            status_code=400
        )

    if not password_pattern.match(password):
        return False, dict(
            reason="Password must be between 8 and 32 characters, contain at least 1 uppercase letter, 1 lowercase letter, and 1 number",
            status_code=400
        )

    adapter = AccountManager(username, password)
    flag = adapter.check_account()
    if flag:
        return False, dict(
            reason="Username already exists",
            status_code=400
        )

    flag = adapter.create_account()
    if flag:
        return True, dict(
            status_code=201
        )
    else:
        return False, dict(
            reason="Create User Failed",
            status_code=400
        )


def verify_account_impl(username, password):
    if not username or not password:
        return False, dict(
            reason="Username and password are required",
            status_code=400
        )

    adapter = AccountManager(username, password)
    flag = adapter.check_failed_attempts()
    if not flag:
        return False, dict(
            reason="Too many failed attempts. Please wait one minute before trying again.",
            status_code=400
        )

    flag = adapter.check_user_password()
    if not flag:
        return False, dict(
            reason="Invalid username or password",
            status_code=401
        )
    else:
        return True, dict(
            status_code=200
        )

