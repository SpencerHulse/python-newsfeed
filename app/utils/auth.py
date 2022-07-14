from flask import session, redirect
from functools import wraps


def login_required(func):
    @wraps(func)
    def wrapped_function(*args, **kwargs):
        # If logged in, call original function with original arguments
        if session.get("loggedIn") == True:
            return func(*args, **kwargs)
        # Otherwise, redirect
        return redirect("/login")

    return wrapped_function
