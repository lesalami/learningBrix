from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired


class LoginForm(Form):
    """Login form to access writing and settings pages"""

    email = StringField('email', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])