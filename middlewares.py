from flask import session, redirect, url_for, flash

def login_required(func):
    def wrapper(*args, **kwargs):
        if not session.get('logged_in'):
            flash('Please login first!', 'warning')
            return redirect(url_for('login_route'))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper
