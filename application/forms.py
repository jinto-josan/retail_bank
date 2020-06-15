from flask_wtf import FlaskForm,Form
# Use this documentation as required for things
#https://wtforms.readthedocs.io/en/2.3.x/
from wtforms import StringField,PasswordField,SubmitField,TextField,RadioField
#https://stackoverflow.com/questions/53449992/flask-wtforms-integerfield-type-is-text-instead-of-number
from wtforms.validators import InputRequired,EqualTo,Length
from wtforms import StringField,FieldList,FormField
from wtforms.widgets import TextArea
from wtforms.fields import html5 as fld5 #for html5 we need this
from wtforms.widgets import html5 as wdgt5
