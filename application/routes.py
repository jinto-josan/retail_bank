'''
To define all the routes
'''
from application import app
from flask import render_template,flash,redirect,request,url_for,jsonify
from sqlalchemy import text

from application.forms import LoginForm, CreateAccountForm, DeleteAccountForm, CustomerQueryForm
from application import db
from application.db_models import Userstore, Customer, Accounts
import datetime

# db.session.commit()
# db.drop_all()
# db.create_all()
# db.session.add(Userstore(loginid='executive',password='executive',user_type='E'))
# db.session.add(Userstore(loginid='cashier',password='cashier',user_type='C'))
# db.session.commit()
'''db.drop_all()
db.create_all()
db.session.add(Userstore(loginid='executive',password='executive',user_type='E'))
db.session.add(Userstore(loginid='cashier',password='cashier',user_type='C'))
db.session.add(Customer(customer_id='123456789',customer_ssn='123456789',customer_name='Jinto',age=23,address_lane_1='xyz',address_lane_2='xyz',city='xyz',status='xyz',message='xyz'))
db.session.commit()
'''

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
            if user_type[0] == 'E':
                return redirect(url_for('create_customer'))
            else:
                return redirect(url_for('account_details'))
    return render_template('login.html', form = form)


@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        try:
            customer_id = request.values.get("customer_id")
            customer_ssn = request.values.get('customer_ssn')
            customer_name = request.values.get('customer_name')
            age = request.values.get('age')
            address1 = request.values.get('address1')
            address2 = request.values.get('address2')
            city = request.values.get("city")
            state = request.values.get("state")
            # status = request.values.get("status")
            message = request.values.get("message")
            db.session.add(Customer(customer_id=customer_id, customer_ssn=customer_ssn, customer_name=customer_name,
                                    age=age, address_lane_1=address1, address_lane_2=address2, city=city, state=state,
                                    message=message))
            db.session.commit()
            flash('Customer creation initiated successfully !')
            return render_template('customer_executive_layout.html')
        except Exception:
            flash('Customer creation error')
            return redirect(url_for('create_customer'))
    else:
        return render_template('create_customer.html')


@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    if request.method == 'POST':
        if len(list(request.values)) == 2:
            try:
                if len(request.values.get('customer_id')):
                    sql = text("SELECT * FROM customers WHERE customer_id = :x")
                    result = db.engine.execute(sql, x=request.values.get("customer_id"))
                else:
                    sql = text("SELECT * FROM customers WHERE customer_ssn = :x")
                    result = db.engine.execute(sql, x=request.values.get("customer_ssn"))
                data = []
                for i in result:
                    data.append(('customer_id', i.customer_id))
                    data.append(('customer_ssn', i.customer_ssn))
                    data.append(('old age', i.age))
                    data.append(('old state', i.state))
                    data.append(('old customer_name', i.customer_name))
                    data.append(('old address 1', i.address_lane_1))
                    data.append(('old address 2', i.address_lane_2))
                    data.append(('old city', i.city))
                return render_template('update_customer_details.html', data=data)
            except Exception as e:
                print(e)
                flash('there is no such customer with that id')
                return render_template('update_customer.html')
        else:
            customer_id = request.values.get('customer_id')
            c = 0
            if len(request.values.get('customer_name')) >= 1:
                sql = text('update customers set {} = :x where customer_id = :y'.format('customer_name'))
                db.engine.execute(sql, x=request.values.get('customer_name'), y=customer_id)
                c += 1
            if len(str(request.values.get('age'))) >= 1:
                sql = text('update customers set {} = :x where customer_id = :y'.format('age'))
                db.engine.execute(sql, x=request.values.get('age'), y=customer_id)
                c += 1
            if len(request.values.get('address_lane_1')) >= 1:
                sql = text('update customers set {} = :x where customer_id = :y'.format('address_lane_1'))
                db.engine.execute(sql, x=request.values.get('address_lane_1'), y=customer_id)
                c += 1
            if len(request.values.get('address_lane_2')) >= 2:
                sql = text('update customers set {} = :x where customer_id = :y'.format('address_lane_2'))
                db.engine.execute(sql, x=request.values.get('address_lane_2'), y=customer_id)
                c += 1
            if len(request.values.get('city')) >= 1:
                sql = text('update customers set {} = :x where customer_id = :y'.format('city'))
                db.engine.execute(sql, x=request.values.get('city'), y=customer_id)
                c += 1
            if len(request.values.get('state')) >= 1:
                sql = text('update customers set {} = :x where customer_ssnid = :y'.format('state'))
                db.engine.execute(sql, x=request.values.get('state'), y=customer_id)
                c += 1
            if c:
                flash('your updates are in progress')
            else:
                flash("you didn't make any changes")
            return render_template('customer_executive_layout.html')
    else:
        return render_template('update_customer.html')


@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if request.method == 'POST':
        if len(list(request.values)) == 1:
            sql = text("SELECT * FROM customers WHERE customer_id = :x")
            result = db.engine.execute(sql, x=request.values.get("customer_id"))
            data = []
            for i in result:
                data.append(('customer_id', i.customer_id))
                data.append(('customer_ssn', i.customer_ssn))
                data.append(('old age', i.age))
                data.append(('old state', i.state))
                data.append(('old customer_name', i.customer_name))
                data.append(('old address 1', i.address_lane_1))
                data.append(('old address 2', i.address_lane_2))
                data.append(('old city', i.city))
            return render_template('confirm_delete_customer.html', data=data)
        else:
            sql = text("DELETE FROM customers WHERE customer_id = :x")
            db.engine.execute(sql, x=request.values.get('customer_id'))
            flash('customer deleted')
            return render_template('customer_executive_layout.html')
    else:
        return render_template('delete_customer.html')


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
                db.session.add(Accounts(customer_id=customer_id, account_id=account_id, account_type=account_type,
                                        balance=dep_amt, message='Initiated Successfully', status='Completed',balance_credit_debit='0Cr',
                                        last_updated=datetime.datetime.now()))
                db.session.commit()
            else:
                flash('Account Id already exists')
            return redirect(url_for('create_account'))
    else:
        for key in form.errors:
            flash('Invalid '+ form.errors[key])
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
def get_type(account_id):
    response = [row[0] for row in db.engine.execute("SELECT account_type FROM accounts WHERE account_id= :x",x=account_id)][0]
    response_obj={'account_type':response}
    return jsonify(response_obj)


@app.route('/status_account',methods=['GET','POST'])
def status_account():
    rslt = db.engine.execute("SELECT customer_id,account_type,status,message,last_updated,account_id FROM accounts")
    rows = [row for row in rslt]
    return render_template('status_account.html',accounts=rows)

@app.route('/status_particular/<account_id>',methods=['GET','POST'])
def status_particular(account_id):
    rslt = db.engine.execute("SELECT status,message,last_updated FROM accounts WHERE account_id =:x",x=account_id)
    row = [item for item in rslt][0]
    response_obj={'status':row[0],'message':row[1],'last_updated':row[2]}
    return jsonify(response_obj)


@app.route('/account_details',methods=['GET','POST'])
def account_details():
    return render_template('account_details.html')
