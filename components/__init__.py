from components.user import User, UserModel
from components.form import Form, FormModel
from components.submit import Submit, SubmitModel
from db import engine, Base


Base.metadata.create_all(engine)
