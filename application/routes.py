'''
To define all the routes
'''
from application import app
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
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        id = Userstore.query.filter_by(loginid=form.login.data).first()
        print(id)
        form.login.data=''
        if id==None:
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
