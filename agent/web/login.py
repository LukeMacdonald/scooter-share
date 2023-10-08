from functools import wraps
from flask import redirect, url_for, session

def user_login_req(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_info' not in session:
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return decorated_function

def eng_login_req(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'eng_info' not in session:
            return redirect(url_for('user.login'))
        return func(*args, **kwargs)
    return decorated_function