'''
To define all the routes
'''
from application import app
from flask import render_template,flash,redirect,request,url_for
from application.forms import LoginForm
from application import db
from application.db_models import Userstore
db.drop_all()
db.create_all()
db.session.add(Userstore(loginid='admin',password='admin'))
db.session.add(Userstore(loginid='jinto',password='password'))
db.session.commit()

@app.route('/',methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        id = Userstore.query.filter_by(loginid=form.login.data).first()
        print(id)
        form.login.data=''
        if id == None:
            flash('Login id not available')
        else:
            password = Userstore.query.filter_by(password=form.password.data).first()
            if password == None:
                flash('Incorrect Password')
            else:
                return redirect(url_for('check_login'))
    '''else:
      flash('All fields are required.')'''
    return render_template('login.html', form = form)


@app.route('/check_login',methods = ['GET', 'POST'])
def check_login():
    if request.method == "POST":
        req = request.form
        print(req)
