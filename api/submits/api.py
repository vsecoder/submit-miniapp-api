from sanic import Blueprint
import pydantic
from components import User, Form, Submit, SubmitModel
from pprint import pprint
from sanic.response import json
from sqlalchemy.exc import IntegrityError
from sanic.log import logger as log
from utils.decorators.auth import protect
from datetime import *
from sanic_openapi import openapi


api = Blueprint('submit', url_prefix='/submit')


@openapi.body(
    SubmitModel,
    description='Create submit',
    required=True
)
@api.route('/create', methods=['POST'])
@protect
async def create(request):
    try:
        data = SubmitModel(**request.json)
        event = Form.get(data.event_id)
        if event is None:
            return json({'error': 'Form not found'}, status=404)

        start = datetime.strptime(data.start, '%d.%m.%Y_%H:%M')
        end = datetime.strptime(data.end, '%d.%m.%Y_%H:%M')

        shorts = Submit.create(
            name=data.name,
            description=data.description,
            start=start,
            end=end,
            color=data.color,
            event_id=data.event_id,
            user_id=event.user_id
        )

        return json(shorts.to_json())
    except pydantic.ValidationError as e:
        return json({'error': e.errors()}, status=400)
    except IntegrityError as e:
        log.error(e)
        return json({'error': 'IntegrityError'}, status=400)


@api.route('/get/<short_id:int>', methods=['GET'])
@protect
async def get(request, short_id):
    shorts = Submit.get(short_id)
    if shorts is None:
        return json({'error': 'Submit not found'}, status=404)
    return json(shorts.to_json())


@api.route('/get_all/<event_id:int>', methods=['GET'])
@protect
async def get_all(request, event_id):
    event = Form.get(event_id)
    if event is None:
        return json({'error': 'Form not found'}, status=404)
    shorts = Submit.get_all(event_id)
    return json([short.to_json() for short in shorts])


@api.route('/delete/<short_id:int>', methods=['DELETE'])
@protect
async def delete(request, short_id):
    shorts = Submit.get(short_id)
    if shorts is None:
        return json({'error': 'Submit not found'}, status=404)
    shorts.delete()
    return json({'success': True})


#@openapi.body(
#    SubmitModel,
#    description='Update short',
#    required=True
#)
#@api.route('/update/<short_id:int>', methods=['POST'])
#@protect
#async def update(request, short_id):
#    try:
#        data = SubmitModel(**request.json)
#        shorts = Submit.get(short_id)
#        if shorts is None:
#            return json({'error': 'Su not found'}, status=404)
#
#        shorts.update(**data.dict())
#
#        return json(shorts.to_json())
#    except pydantic.ValidationError as e:
#        return json({'error': e.errors()}, status=400)
#    except IntegrityError as e:
#        log.error(e)
#        return json({'error': 'IntegrityError'}, status=400)
