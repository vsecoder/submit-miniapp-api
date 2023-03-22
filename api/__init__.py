from api.user.api import api as user_api
from api.forms.api import api as forms_api
from api.submits.api import api as submits_api
from api.auth.api import api as auth_api
from sanic import Blueprint


api = Blueprint.group(auth_api, user_api, forms_api, submits_api, url_prefix='/api')