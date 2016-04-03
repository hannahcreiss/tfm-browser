from wtforms import Form, TextField, PasswordField, validators
from models import User


class LoginForm(Form):
    username = TextField(u'username', validators=[validators.input_required()])
    password = PasswordField(u'password', validators=[validators.input_required()])