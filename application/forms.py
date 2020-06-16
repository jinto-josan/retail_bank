'''
To define all the forms for data input
'''
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length



class LoginForm(FlaskForm):
    login = StringField("Login Id",render_kw={'Placeholder':'Login Id'})
    password = PasswordField("Password", render_kw={'Placeholder':'Password'})
    submit = SubmitField("Login")

class CreateAccountForm(FlaskForm):
    login = StringField("Login Id",render_kw={'Placeholder':'Login Id'})
    password = PasswordField("Password", render_kw={'Placeholder':'Password'})
    submit = SubmitField("Login")

class AccountQueryForm(FlaskForm):
    login = StringField("Login Id",render_kw={'Placeholder':'Login Id'})
    password = PasswordField("Password", render_kw={'Placeholder':'Password'})
    submit = SubmitField("Login")
