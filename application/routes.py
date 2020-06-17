'''
To define all the routes
'''
from application import app
from flask import render_template,flash,redirect,request,url_for,jsonify
from sqlalchemy import text
import datetime

from application.forms import LoginForm,CreateAccountForm,CustomerQueryForm,DeleteAccountForm
from application import db
from application.db_models import Userstore,Customer,Accounts
'''db.drop_all()
db.create_all()
db.session.add(Userstore(loginid='executive',password='executive',user_type='E'))
db.session.add(Userstore(loginid='cashier',password='cashier',user_type='C'))
db.session.add(Customer(customer_id='123456789',customer_ssn='123456789',customer_name='Jinto',age=23,address_lane_1='xyz',address_lane_2='xyz',city='xyz',status='xyz',message='xyz'))
db.session.commit()'''

@app.route('/',methods = ['GET','POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        sql = text( "SELECT user_type FROM userstore WHERE loginid = :x AND password = :y")
        rslt = db.engine.execute(sql,x=form.login.data,y=form.password.data)
        user_type = [row[0] for row in rslt]
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
            #print(e)
            flash('Customer creation error')
            #out = {'success': False, 'message': "some error occurred while creating user"}
            #return jsonify(out)
        return redirect(url_for('create_customer'))
    else:
        return render_template('create_customer.html')


@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    form = CreateAccountForm()
    if form.validate_on_submit():
        sql = text( "SELECT  customer_name FROM customers WHERE customer_id = :x ")
        rslt = db.engine.execute(sql,x=form.customer_id.data)
        name = [row[0] for row in rslt]
        if len(name) == 0:
            flash('Customer Id not found !')
        else:
            acnt_sql = text( "SELECT  customer_id FROM accounts WHERE account_id = :x ")
            acnt_rslt = db.engine.execute(acnt_sql,x=form.account_id.data)
            if len([row[0] for row in acnt_rslt]) == 0:
                flash('Account creation initiated successfully')
                customer_id=form.customer_id.data
                account_id =form.account_id.data
                account_type =form.account_type.data
                dep_amt = form.dep_amt.data
                db.session.add(Accounts(customer_id=customer_id, account_id=account_id, account_type=account_type, balance=dep_amt, \
                                message='Initiated Successfully', status='Completed',last_updated=datetime.datetime.now()))
                db.session.commit()
            else:
                flash('Account already exists')
            return redirect(url_for('create_account'))
    else:
        for key in form.errors:
            flash('Invalid '+ key)
    return render_template('create_account.html', form = form)


@app.route('/query_customer', methods=['GET', 'POST'])
def query_customer():
    form = CustomerQueryForm()
    if form.validate_on_submit():
        cid= form.customer_id.data
        ssn= form.ssn.data
        if (ssn==None) ^ (cid==None):
            sql = text( "SELECT customer_id FROM customers WHERE customer_id = :x or customer_ssn =:y")
            rslt = db.engine.execute(sql,x=cid,y=ssn)
            id = [row[0] for row in rslt]
            if len(id) == 0:
                flash('Customer Id or Customer SSN not found !')
            else:
                return redirect(url_for('delete_account',idx=id))
        else:
            flash('Please provide either customer id or ssid')
        return redirect(url_for('query_customer'))
    else:
        for key in form.errors:
            flash('Invalid '+ key)
    return render_template('query_customer.html', form = form)





@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    form = DeleteAccountForm()
    cid = int(request.args.get('idx'))
    sql = text( "SELECT  account_id FROM accounts WHERE customer_id= :x")
    rslt = db.engine.execute(sql,x=cid)
    ids = [row[0] for row in rslt]
    chcs = list(zip(ids,ids))
    print(chcs)
    form.account_id_choices.choices= chcs
    form.account_type.data = [row[0] for row in db.engine.execute("SELECT account_type FROM accounts WHERE account_id= :x",x=chcs[0][0])][0]
    if form.validate_on_submit():
        print('deleted')
        db.engine.execute("DELETE FROM accounts WHERE account_id= :x",x=form.account_id_choices.data)
        db.session.commit()
        flash('Account deletion initiated successfully')
        return redirect(url_for('delete_account',idx=cid))
    else:
        for key in form.errors:
            flash('Invalid '+ key)
    return render_template('delete_account.html', form = form)

@app.route('/get_type/<account_id>',methods=['GET','POST'])
def get_status(account_id):
    response = [row[0] for row in db.engine.execute("SELECT account_type FROM accounts WHERE account_id= :x",x=account_id)][0]
    response_obj={'account_type':response}
    return jsonify(response_obj)
