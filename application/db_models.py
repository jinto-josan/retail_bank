from application import db

class Userstore(db.Model):
    __tablename__='userstore'
    login= db.column(db.String(64),primary_key=True)
    password= db.column(db.String(64))
    timestamp= db.column(db.DateTime('YYYY-MM-DDTHH:MM:SS'))
