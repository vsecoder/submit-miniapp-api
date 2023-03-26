from sanic import Blueprint
import pydantic
from components import Form, FormModel
from pprint import pprint
from sanic.response import json
from sqlalchemy.exc import IntegrityError
from sanic.log import logger as log
from utils.decorators.auth import protect
from datetime import *
from sanic_openapi import openapi
api = Blueprint('form', url_prefix='/form')


@api.route('/ping', methods=['GET'])
@protect
async def ping(request):
    return json({'message': 'pong'})


@openapi.summary('Create form')
@openapi.description('Create form')
@openapi.body(FormModel, description='Form model', required=True)
@api.route('/create', methods=['POST'])
@protect
async def create(request):
    try:
        data = request.json
        log.debug(data)
        user = request.ctx.user
        event = FormModel(**data, user_id=user.id)
        event = Form.create(**event.dict())
        return json({'message': 'Form created', 'form': event.to_json()})
    except IntegrityError as e:
        log.error(e)
        return json({'message': 'error'}, status=500)
    except pydantic.ValidationError as e:
        log.error(e)
        return json({'message': 'error'}, status=500)


@api.route('/getAll', methods=['GET'])
@protect
async def getAll(request):
    user = request.ctx.user
    events = user._forms
    return json({'Forms': [event.to_json() for event in events]})


@api.route('/get/<id>', methods=['GET'])
@protect
async def get(request, id):
    user = request.ctx.user
    event = Form.get(id=id)
    return json({'event': event.to_json()})


@api.route('/update/<id>', methods=['POST'])
@protect
async def update(request, id):
    try:
        data = request.json
        log.debug(data)
        event = Form.get(id=id)
        event.edit(**data)
        return json({'message': 'Form updated', 'event': event.to_json()})
    except IntegrityError as e:
        log.error(e)
        return json({'message': 'error'}, status=500)
    except pydantic.ValidationError as e:
        log.error(e)
        return json({'message': 'error'}, status=500)


@api.route('/delete/<id>', methods=['DELETE'])
@protect
async def delete(request, id):
    try:
        event = Form.get(id=id)
        event.delete()
        return json({'message': 'Form deleted'})
    except IntegrityError as e:
        log.error(e)
        return json({'message': 'error'}, status=500)
    except pydantic.ValidationError as e:
        log.error(e)
        return json({'message': 'error'}, status=500)

