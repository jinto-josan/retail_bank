'''
To define all the forms for data input
'''
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import InputRequired, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    login = StringField("Login Id", validators=[InputRequired()], render_kw={'Placeholder': 'Login Id'})
    password = PasswordField("Password", validators=[InputRequired()], render_kw={'Placeholder': 'Password'})
    submit = SubmitField("Login")


class CreateAccountForm(FlaskForm):
    customer_id = IntegerField("Customer Id", validators=[InputRequired(), NumberRange(min=100000000, max=999999999)],
                               render_kw={'Placeholder': 'Customer Id'})
    account_id = IntegerField("Account Id", validators=[InputRequired(), NumberRange(min=100000000, max=999999999)],
                              render_kw={'Placeholder': 'Account Id'})
    account_type = SelectField("Account Type", choices=[('S', 'Savings'), ('C', 'Current')],
                               render_kw={'Placeholder': 'Select'})
    dep_amt = IntegerField("Deposit Amount", default=0,
                           validators=[InputRequired(message='Customer Id required'),
                                       NumberRange(min=0, message='Amount shouldnot be negitive')],
                           render_kw={'Placeholder': 'Amount'})
    submit = SubmitField("Submit")


class CustomerQueryForm(FlaskForm):
    customer_id = IntegerField("Customer Id", validators=[Optional(), NumberRange(min=100000000, max=999999999)],
                               render_kw={'Placeholder': 'Customer Id'})
    ssn = IntegerField("Customer SSN", validators=[Optional(), NumberRange(min=100000000, max=999999999)],
                       render_kw={'Placeholder': 'SSN'})
    submit = SubmitField("Submit")


class DeleteAccountForm(FlaskForm):
    account_id_choices = SelectField("Account ID", coerce=int, choices=[], render_kw={'Placeholder': 'Select'})
    account_type = StringField("Account Type", default='Savings', render_kw={'Placeholder': 'Select'})
    submit = SubmitField("Delete")


class AccountQueryForm1(FlaskForm):
    customer_id = IntegerField("Customer Id", validators=[Optional(), NumberRange(min=100000000, max=999999999)],
                               render_kw={'Placeholder': 'Customer Id'})
    ssn = IntegerField("Customer SSN", validators=[Optional(), NumberRange(min=100000000, max=999999999)],
                       render_kw={'Placeholder': 'SSN'})
    account_id = IntegerField("Account Id", validators=[Optional(), NumberRange(min=100000000, max=999999999)],
                              render_kw={'Placeholder': 'Account ID'})
    submit = SubmitField("Submit")


class TransactionForm(FlaskForm):
    account_id_choices = SelectField("Account ID", coerce=int, choices=[], render_kw={'Placeholder': 'Select'})
    deposit = SubmitField("Deposit")
    withdraw = SubmitField("Withdraw")
    transfer = SubmitField("Transfer")
