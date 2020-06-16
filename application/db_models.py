from application import db


class Userstore(db.Model):
    __tablename__ = 'userstore'
    login = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64))
    user_type = db.Column(db.String(64))
    timestamp = db.Column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))


class Customer(db.Model):
    __tablename__ = 'customers'
    # as per pdf 5.1.9 option 1
    sno = db.Column(db.Integer, primary_key=True)
    customer_ssnid = db.Column(db.Integer)
    customer_name = db.Column(db.String(64))
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.accounts_id'))
    age = db.Column(db.Integer)
    address_lane_1 = db.Column(db.String(64))
    address_lane_2 = db.Column(db.String(64))
    city = db.Column(db.String(64))
    state = db.Column(db.String(64))
    balance = db.Column(db.Integer)
    account_type = db.Column(db.String(64))
    status = db.Column(db.String(64))
    message = db.Column(db.String(64))
    last_updated = db.Column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))


class Accounts(db.Model):
    __tablename__ = 'accounts'
    sno = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, index=True)
    balance = db.Column(db.Integer)
    balance_added = db.Column(db.Integer)
    balance_deducted = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))




