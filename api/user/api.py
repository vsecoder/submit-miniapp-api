from sanic import Blueprint
import pydantic
from components import User, UserModel
from pprint import pprint
from sanic.response import json
from sqlalchemy.exc import IntegrityError
from sanic.log import logger as log
from utils.decorators.auth import protect
from sanic_openapi import openapi
api = Blueprint('user', url_prefix='/user')


@openapi.body(
    UserModel,
    description='Create user',
    required=True
)
@api.route('/create', methods=['POST'])
async def register(request):
    data = request.json
    try:
        user = UserModel(**data)
        user = User.create(**user.dict())
        return json(user.to_json())
    except pydantic.ValidationError as e:
        log.error(e)
        return json({'error': e.errors()}, status=400)
    except Exception as e:
        return json({'error': str(e)}, status=400)


@api.route('/get', methods=['GET'])
@protect
async def get(request):
    user = request.ctx.user
    return json(user.to_json())