

from functools import wraps
from flask import redirect, url_for, session

def admin_login_req(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'admin_info' not in session:
            return redirect(url_for('admin.index'))
        return func(*args, **kwargs)
    return decorated_function