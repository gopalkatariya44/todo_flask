from functools import wraps
from flask import session, redirect, url_for, flash


def secured_endpoint(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        # Check if user is logged in or session data indicates security
        if 'user_id' not in session:
            flash('You need to be logged in to access this page.', 'warning')
            return redirect(url_for('user_login'))  # Redirect to login page if not logged in
        user_id = session['user_id']
        return func(user_id, *args, **kwargs)

    return decorated_function
