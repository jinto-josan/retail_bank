'''
To define all the forms for data input
'''
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,IntegerField
from wtforms.validators import InputRequired,Length,NumberRange



class LoginForm(FlaskForm):
    login = StringField("Login Id",validators=[InputRequired(),Length(max=30,message='Maximum 15 characters')],render_kw={'Placeholder':'Login Id'})
    password = PasswordField("Password",validators=[InputRequired(),Length(max=15,message='Maximum 15 characters')], render_kw={'Placeholder':'Password'})
    submit = SubmitField("Login")

class CreateAccountForm(FlaskForm):
    login = StringField("Login Id",render_kw={'Placeholder':'Login Id'})
    password = PasswordField("Password", render_kw={'Placeholder':'Password'})
    submit = SubmitField("Login")

class CustomerQueryForm(FlaskForm):
    customerid = IntegerField("Customer Id",validators=[NumberRange(min=100000000,max=999999999)],render_kw={'Placeholder':'Customer Id'})
    ssnid = PasswordField("Password", render_kw={'Placeholder':'Password'})
    submit = SubmitField("Login")
