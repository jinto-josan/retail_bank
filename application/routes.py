'''
To define all the routes
'''
from application import app
from flask import render_template,flash,redirect,request,url_for
from sqlalchemy import and_
from sqlalchemy import text
from application.forms import LoginForm
from application import db
from application.db_models import Userstore
'''db.drop_all()
db.create_all()
db.session.add(Userstore(loginid='admin',password='password',user_type='E'))
db.session.add(Userstore(loginid='king',password='admin',user_type='C'))
db.session.commit()'''

@app.route('/',methods = ['GET','POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sql = text( "SELECT user_type FROM userstore WHERE loginid = :x AND password = :y")
        rslt = db.engine.execute(sql,x=form.login.data,y=form.password.data)
        user_type = [row[0] for row in rslt ]
        #id = Userstore.query.filter(and_(Userstore.loginid == form.login.data,Userstore.password==form.password.data)).first()
        form.login.data=''
        if len(user_type) == 0:
            flash('Entered Login ID or Password is Wrong !')
        else:
            if(user_type[0] == 'E'):
                return redirect(url_for('create_customer'))
            else:
                return redirect(url_for('cashier'))
    return render_template('login.html', form = form)

@app.route('/create-customer')
def create_customer():
    return render_template('create_customer.html')

@app.route('/cashier')
def cashier():
    pass
