from functools import wraps
from sanic.response import json
from components.user import User
from sanic.log import logger as log
import jwt
from config import Config
from pprint import pprint

def auth_required():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = request.headers.get('Authorization')
            if not token:
                return json({'error': 'Token not found'}, status=400)
            user = User.get_by_token(token)
            if not user:
                return json({'error': 'Token not found'}, status=400)
            return await f(request, user, *args, **kwargs)
        return decorated_function
    return decorator


def protect(f):
    @wraps(f)
    async def wrapper(*args, **kwargs):
        request = args[0]
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return json({"error": "Authorization header is missing."}, status=401)

        parts = auth_header.split()
        if len(parts) != 2:
            return json({"error": "Authorization header is invalid."}, status=401)

        scheme, token = parts
        if scheme.lower() != "bearer":
            return json({"error": "Authorization header is invalid."}, status=401)

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        except Exception as e:
            return json({"error": str(e)}, status=401)

        user = User.get(payload['id'])
        if not user:
            return json({"error": "User not found"}, status=401)
        request.ctx.user = user
        return await f(*args, **kwargs)

    return wrapper
