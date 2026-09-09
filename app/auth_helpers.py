from functools import wraps
from flask import session, jsonify

def api_login_required(view_function):
    """Reject unauthenticated requests with 401 and a JSON body."""
    @wraps(view_function)
    def wrapped_view(*args, **kwargs):
        if "user_id" not in session:
            return jsonify({"error": "Authentication required"}), 401
        return view_function(*args, **kwargs)

    return wrapped_view