from application import db


class Userstore(db.Model):
    __tablename__ ='userstore'
    loginid = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64))
    user_type = db.Column(db.String(64))
    #timestamp = db.Column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))


class Customer(db.Model):
    __tablename__ = 'customers'
    # as per pdf 5.1.9 option 1
    # sno = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, primary_key=True)
    customer_ssn = db.Column(db.Integer, unique=True, index=True)
    customer_name = db.Column(db.String(64))
    # account_id = db.Column(db.Integer, db.ForeignKey('accounts.accounts_id'))
    age = db.Column(db.Integer)
    address_lane_1 = db.Column(db.String(64))
    address_lane_2 = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    # balance = db.Column(db.Integer)
    # account_type = db.Column(db.String(64))
    status = db.Column(db.String(64))
    message = db.Column(db.String(64))
<<<<<<< HEAD



=======
>>>>>>> master
    last_updated = db.Column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))


class Accounts(db.Model):
    __tablename__ = 'accounts'
    sno = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
<<<<<<< HEAD
    request = db.relationship("Customer") # if this is not done then customer id wont be displayed in the accounts table
=======
    request = db.relationship("Customer")
    # if this is not done then customer id wont be displayed in the accounts table
>>>>>>> master
    account_id = db.Column(db.Integer, index=True)
    balance = db.Column(db.Integer)
    balance_credit_debit = db.Column(db.String(64))
    # balance_deducted = db.Column(db.Integer)
    account_type = db.Column(db.String(64))
    message = db.Column(db.String(64))
    status = db.Column(db.String(64))
    last_updated = db.Column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))
