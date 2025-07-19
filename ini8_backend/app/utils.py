import jwt
from flask import request, current_app, jsonify
from functools import wraps

def generate_token(user_id):
    return jwt.encode({"user_id": user_id}, current_app.config["SECRET_KEY"], algorithm="HS256")

def verify_token(token):
    return jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
        token = auth.replace("Bearer ", "")
        try:
            verify_token(token)
        except Exception:
            return jsonify({"error": "Invalid or expired token"}), 401
        return f(*args, **kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf'
