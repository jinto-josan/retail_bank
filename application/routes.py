'''
To define all the routes
'''
from application import app
<<<<<<< HEAD
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
=======
from flask import render_template,flash,redirect,request,url_for, jsonify
from application.forms import LoginForm
from application import db
from application.db_models import Userstore, Accounts, Customer
db.drop_all()
db.create_all()
db.session.add(Userstore(loginid='admin', password='admin', user_type='accountexec'))
db.session.add(Userstore(loginid='cashier', password='teller', user_type='cashier'))
db.session.commit()


@app.route('/', methods = ['GET'])
>>>>>>> bee3b940f5b34218854a2c6530afafd7e055cb6a
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sql = text( "SELECT user_type FROM userstore WHERE loginid = :x AND password = :y")
        rslt = db.engine.execute(sql,x=form.login.data,y=form.password.data)
        user_type = [row[0] for row in rslt ]
        #id = Userstore.query.filter(and_(Userstore.loginid == form.login.data,Userstore.password==form.password.data)).first()
        form.login.data=''
<<<<<<< HEAD
        if len(user_type) == 0:
            flash('Entered Login ID or Password is Wrong !')
=======
        if id==None:
            flash('Login id not available')
>>>>>>> bee3b940f5b34218854a2c6530afafd7e055cb6a
        else:
            if(user_type[0] == 'E'):
                return redirect(url_for('create_customer'))
            else:
                return redirect(url_for('cashier'))
    return render_template('login.html', form = form)

@app.route('/create-customer')
def create_customer():
    return render_template('create_customer.html')

<<<<<<< HEAD
@app.route('/cashier')
def cashier():
    pass
=======
@app.route('/check_login',methods = ['GET', 'POST'])
def check_login():
    if request.method == "POST":
        req = request.form
        print(req)


@app.route('/createuser', methods=['GET', 'POST'])
def createuser():
    if request.method == 'POST':
        # print(request.values)
        try:
            customer_ssnid = request.values.get("customer_ssnid")
            # print(customer_ssnid)
            customer_name = request.values.get('customer_name')
            age = request.values.get('age')
            address1 = request.values.get('address1')
            address2 = request.values.get('address2')
            city = request.values.get("city")
            state = request.values.get("state")
            # status = request.values.get("status")
            message = request.values.get("message")
            db.session.add(Customer(customer_ssnid=customer_ssnid, customer_name=customer_name, age=age,
                                    address_lane_1=address1, address_lane_2=address2, city=city, state=state,
                                    message=message))
            out = {'success': True, 'message': "Customer creation initiated successfully"}
            # response = JsonResponse(out)
            # response["Access-Control-Allow-Origin"] = "*"
            # response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            # response["Access-Control-Max-Age"] = "1000"
            # response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
            return jsonify(out)
            # return render_template()
        except Exception as e:
            print(e)
            out = {'success': False, 'message': "some error occurred while creating user"}
            return jsonify(out)
    else:
        return render_template('create_user.html')
>>>>>>> bee3b940f5b34218854a2c6530afafd7e055cb6a
