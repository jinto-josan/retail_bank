from application import db


class Userstore(db.Model):
    __tablename__ = 'userstore'
    login = db.column(db.String(64), primary_key=True)
    password = db.column(db.String(64))
    timestamp = db.column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))


class Customer(db.Model):
    __tablename__ = 'customers'
    # as per pdf 5.1.9 option 1
    customer_ssnid = db.column(db.Integer)
    customer_name = db.column(db.string(64))
    account_id = db.column(db.Integer, db.ForeignKey('accounts.accounts_id'))
    age = db.column(db.Integer)
    address_lane_1 = db.column(db.string(64))
    address_lane_2 = db.column(db.string(64))
    city = db.column(db.string(64))
    state = db.column(db.string(64))
    balance = db.column(db.Integer)
    account_type = db.column(db.string(64))
    status = db.column(db.string(64))
    message = db.column(db.string(64))
    last_updated = db.DateTime(db.ForeignKey('accounts.timestamp'))


class Accounts(db.Model):
    __tablename__ = 'accounts'
    account_id = db.column(db.Integer, index=True)
    balance = db.column(db.Integer)
    balance_added = db.column(db.Integer)
    balance_deducted = db.column(db.Integer)
    timestamp = db.column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))




