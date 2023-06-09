from sanic import Sanic
from sanic.response import json
from db import engine, Base, session
from components import *
from api import *
from config import *
from sanic_cors import CORS, cross_origin
from sanic_openapi import openapi3_blueprint
#from cors import add_cors_headers


app = Sanic(__name__)
app.blueprint(api)
app.blueprint(openapi3_blueprint)
#app.register_middleware(add_cors_headers, "response")
CORS(app)


@app.route('/')
async def test(request):
    return json({'hello': 'world'})


@app.exception(Exception)
async def handle_exception(request, exception):
    session.rollback()
    return json({'error': str(exception)}, status=400)
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True, auto_reload=True)
