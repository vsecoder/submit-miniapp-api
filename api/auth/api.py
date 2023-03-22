from sanic import Blueprint
from components import User
from sanic.response import json
import jwt
from config import Config
from utils.decorators.auth import protect
from sanic_openapi import openapi
api = Blueprint('auth', url_prefix='/auth')

class AuthModel:
    vk_id: int


@api.route("/login", methods=["POST"])
@openapi.body(
    AuthModel,
    description='Login',
    required=True
)
async def auth(request):
    try:
        data = request.json
        if data['vk_id']:
            user = User.get(id=data['vk_id'])
            if user:
                token = jwt.encode({'vk_id': user.id}, Config.SECRET_KEY, algorithm='HS256')
                return json({'token': str(token)})
            else:
                return json({'error': 'User not found'}, status=404)
        else:
            return json({'error': 'Bad request'}, status=400)

    except Exception as e:
        return json({'error': str(e)}, status=400)


@api.route('/check', methods=['POST'])
@protect
async def check(request):
    user = request.ctx.user
    return json({'user_id': user.id})