'''
To define all the routes
'''
from application import app
from flask import render_template,flash,redirect,request,url_for,jsonify
from sqlalchemy import and_
from sqlalchemy import text
from application.forms import LoginForm
from application import db
from application.db_models import Userstore,Customer
'''db.drop_all()
db.create_all()
db.session.add(Userstore(loginid='executive',password='executive',user_type='E'))
db.session.add(Userstore(loginid='cashier',password='cashier',user_type='C'))
db.session.commit()'''

@app.route('/',methods = ['GET','POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sql = text( "SELECT user_type FROM userstore WHERE loginid = :x AND password = :y")
        print(form.login.data)
        print(form.password.data)
        rslt = db.engine.execute(sql,x=form.login.data,y=form.password.data)
        user_type = [row[0] for row in rslt]
        #id = Userstore.query.filter(and_(Userstore.loginid == form.login.data,Userstore.password==form.password.data)).first()
        form.login.data=''
        print(user_type)
        if len(user_type) == 0:
            flash('Entered Login ID or Password is Wrong !')
        else:
            if(user_type[0] == 'E'):
                return redirect(url_for('create_customer'))
            else:
                return redirect(url_for('cashier'))
    return render_template('login.html', form = form)


@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
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
            db.session.commit()
            flash('Customer creation initiated successfully !')
            # response = JsonResponse(out)
            # response["Access-Control-Allow-Origin"] = "*"
            # response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            # response["Access-Control-Max-Age"] = "1000"
            # response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
            #return jsonify(out)
            # return render_template()
        except Exception as e:
            print(e)
            flash('Customer creation error')
            #out = {'success': False, 'message': "some error occurred while creating user"}
            #return jsonify(out)
        return render_template('create_customer.html')
    else:
        return render_template('create_customer.html')
