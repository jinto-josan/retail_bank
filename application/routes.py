'''
To define all the routes
'''
from application import app
from flask import render_template,flash,redirect,request,url_for,jsonify,session
from sqlalchemy import text

from application.forms import LoginForm, CreateAccountForm, DeleteAccountForm, CustomerQueryForm, AccountQueryForm1,TransactionForm
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
db.session.add(Customer(customer_id='123456789',customer_ssn='123456789',customer_name='Jinto',age=23,address_lane_1='xyz',address_lane_2='xyz',city='xyz',status='xyz',message='xyz',last_updated=datetime.datetime.now()))
db.session.commit()'''


@app.route('/',methods = ['GET','POST'])
@app.route('/login', methods = ['GET', 'POST'])
def login():
    if 'user_id' in session:
        if session['user_type'] == 'E':
            return redirect(url_for('create_customer'))
        else:
            return redirect(url_for('account_query1'))
    form = LoginForm()
    if form.validate_on_submit():
        sql = text( "SELECT user_type FROM userstore WHERE loginid = :x AND password = :y")
        print(form.login.data)
        print(form.password.data)
        rslt = db.engine.execute(sql,x=form.login.data,y=form.password.data)
        user_type = [row[0] for row in rslt]
        #id = Userstore.query.filter(and_(Userstore.loginid == form.login.data,Userstore.password==form.password.data)).first()
        form.login.data=''
        if len(user_type) == 0:
            flash('Entered Login ID or Password is Wrong !','danger')
        else:
            session['user_id']=form.login.data
            session['user_type']=user_type[0]
            if user_type[0] == 'E':
                return redirect(url_for('create_customer'))
            else:
                return redirect(url_for('account_query1'))
    return render_template('login.html', form = form,title='Login')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id',None)
        session.pop('user_type',None)
        flash('Logged out successfully ','success')
    return redirect(url_for('login'))



@app.route('/create_customer', methods=['GET', 'POST'])
def create_customer():
    if 'user_id' in session and session['user_type'] == 'E':
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
                flash('Customer creation initiated successfully !','success')
                return render_template('customer_executive_layout.html')
            except Exception:
                flash('Customer creation error','danger')
                return redirect(url_for('create_customer'))
        else:
            return render_template('create_customer.html',title='Add Customer')
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))


@app.route('/update_customer', methods=['GET', 'POST'])
def update_customer():
    if 'user_id' in session and session['user_type'] == 'E':
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
                    flash('there is no such customer with that id','danger')
                    return render_template('update_customer.html')
            else:
                customer_id = request.values.get('customer_id')
                c = 0
                if len(request.values.get('customer_name')) >= 1:
                    print(customer_id)
                    sql = text('update customers set {} = :x where customer_id = :y'.format('customer_name'))
                    db.engine.execute(sql, x=request.values.get('customer_name'), y=customer_id)
                    c += 1
                if len(str(request.values.get('age'))) >= 1:
                    print('change age')
                    sql = text('update customers set {} = :x where customer_id = :y'.format('age'))
                    db.engine.execute(sql, x=request.values.get('age'), y=customer_id)
                    c += 1
                if len(request.values.get('address_lane_1')) >= 1:
                    print('change address')
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
                    flash('your updates are in progress','success')
                else:
                    flash("you didn't make any changes",'primary')
                return render_template('customer_executive_layout.html')
        else:
            return render_template('update_customer.html')
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))



@app.route('/delete_customer', methods=['GET', 'POST'])
def delete_customer():
    if 'user_id' in session and session['user_type'] == 'E':
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
                flash('customer deleted','success')
                return render_template('customer_executive_layout.html')
        else:
            return render_template('delete_customer.html')
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))




@app.route('/create_account', methods=['GET', 'POST'])
def create_account():
    if 'user_id' in session and session['user_type'] == 'E':
        form = CreateAccountForm()
        if form.validate_on_submit():
            sql = text( "SELECT  customer_name FROM customers WHERE customer_id = :x ")
            rslt = db.engine.execute(sql,x=form.customer_id.data)
            name = [row[0] for row in rslt]
            if len(name) == 0:
                flash('Customer Id not found !','danger')
            else:
                acnt_sql = text( "SELECT  customer_id FROM accounts WHERE account_id = :x ")
                acnt_rslt = db.engine.execute(acnt_sql,x=form.account_id.data)
                if len([row[0] for row in acnt_rslt]) == 0:
                    flash('Account creation initiated successfully','success')
                    customer_id=form.customer_id.data
                    account_id =form.account_id.data
                    account_type =form.account_type.data
                    dep_amt = form.dep_amt.data
                    db.session.add(Accounts(customer_id=customer_id, account_id=account_id, account_type=account_type,
                                            balance=dep_amt, message='Initiated Successfully', status='Completed',balance_credit_debit='0Cr',
                                            last_updated=datetime.datetime.now()))
                    db.session.commit()
                else:
                    flash('Account Id already exists','primary')
                return redirect(url_for('create_account'))
        else:
            for key in form.errors:
                flash('Invalid '+ key,'danger')
        return render_template('create_account.html', form = form,title='Create Account')
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))




@app.route('/query_customer', methods=['GET', 'POST'])
def query_customer():
    if 'user_id' in session and session['user_type'] == 'E':
        form = CustomerQueryForm()
        if form.validate_on_submit():
            cid= form.customer_id.data
            ssn= form.ssn.data
            if (ssn==None) ^ (cid==None):
                sql = text( "SELECT customer_id FROM customers WHERE customer_id = :x or customer_ssn =:y")
                rslt = db.engine.execute(sql,x=cid,y=ssn)
                id = [row[0] for row in rslt]
                if len(id) == 0:
                    flash('Customer Id or Customer SSN not found !','danger')
                else:
                    return redirect(url_for('delete_account',ids=id))
            else:
                flash('Please provide either customer id or ssid','primary')
            return redirect(url_for('query_customer'))
        else:
            for key in form.errors:
                flash('Invalid '+ key,'danger')
        return render_template('query_customer.html', form = form)
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))


@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if 'user_id' in session and session['user_type'] == 'E':
        form = DeleteAccountForm()
        cid = int(request.args.get('ids'))
        sql = text( "SELECT  account_id FROM accounts WHERE customer_id= :x")
        rslt = db.engine.execute(sql,x=cid)
        ids = [row[0] for row in rslt]
        chcs = list(zip(ids,ids))
        form.account_id_choices.choices= chcs
        form.account_type.data = [row[0] for row in db.engine.execute("SELECT account_type FROM accounts WHERE account_id= :x",x=chcs[0][0])][0]
        if form.validate_on_submit():
            print('deleted')
            db.engine.execute("DELETE FROM accounts WHERE account_id= :x",x=form.account_id_choices.data)
            db.session.commit()
            flash('Account deletion initiated successfully','success')
            return redirect(url_for('delete_account',idx=cid))
        else:
            for key in form.errors:
                flash('Invalid '+ key,'danger')
        return render_template('delete_account.html', form = form,title='Delete Account')
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))


@app.route('/get_type/<account_id>',methods=['GET','POST'])
def get_type(account_id):
    response = [row[0] for row in db.engine.execute("SELECT account_type FROM accounts WHERE account_id= :x",x=account_id)][0]
    response_obj={'account_type':response}
    return jsonify(response_obj)




@app.route('/status_account',methods=['GET','POST'])
def status_account():
    if 'user_id' in session and session['user_type'] == 'E':
        rslt = db.engine.execute("SELECT customer_id,account_type,status,message,last_updated,account_id FROM accounts")
        rows = [row for row in rslt]
        return render_template('status_account.html',accounts=rows,title='Account Status')
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))

@app.route('/status_account_particular/<account_id>',methods=['GET','POST'])
def status_account_particular(account_id):
    rslt = db.engine.execute("SELECT status,message,last_updated FROM accounts WHERE account_id =:x",x=account_id)
    row = [item for item in rslt][0]
    response_obj={'status':row[0],'message':row[1],'last_updated':row[2]}
    return jsonify(response_obj)



@app.route('/status_customer',methods=['GET','POST'])
def status_customer():
    if 'user_id' in session and session['user_type'] == 'E':
        rslt = db.engine.execute("SELECT customer_ssn,status,message,last_updated,customer_id FROM customers")
        rows = [row for row in rslt]
        return render_template('status_customer.html',accounts=rows,title='Customer Status')
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))

@app.route('/status_customer_particular/<customer_id>',methods=['GET','POST'])
def status_customer_particular(customer_id):
    rslt = db.engine.execute("SELECT status,message,last_updated FROM customers WHERE customer_id =:x",x=customer_id)
    row = [item for item in rslt][0]
    response_obj={'status':row[0],'message':row[1],'last_updated':row[2]}
    return jsonify(response_obj)




@app.route('/account_query1',methods=['GET','POST'])
def account_query1():
    if 'user_id' in session and session['user_type'] == 'C':
        form = AccountQueryForm1()
        if form.validate_on_submit():
            cid= form.customer_id.data
            ssn= form.ssn.data
            aid =form.account_id.data
            if aid == None and ((cid==None) ^ (ssn==None)):
                sql = text( "SELECT customer_id FROM customers WHERE customer_id = :x or customer_ssn =:y")
                rslt = db.engine.execute(sql,x=cid,y=ssn)
                id = [row[0] for row in rslt]
                if len(id) == 0:
                    flash('Customer Id or Customer SSN not found !','danger')
                else:
                    sql = text( "SELECT distinct account_id FROM accounts WHERE customer_id = :z")
                    rslt = db.engine.execute(sql,z=id[0])
                    accounts=  [row[0] for row in rslt]
                    k_v={}
                    for ix,val in enumerate(accounts):
                        k_v.update([('id'+str(ix),val)])
                    return redirect(url_for('choose_transaction',**k_v))
            elif(aid!=None and cid ==None and ssn==None):
                sql = text( "SELECT distinct account_id FROM accounts WHERE account_id = :x")
                rslt = db.engine.execute(sql,x=aid)
                id = [row[0] for row in rslt]
                if len(id) == 0:
                    flash('Account Id not found !','danger')
                else:
                    return redirect(url_for('choose_transaction',id0=id))
            else:
                flash('Please provide either customer id or ssid','primary')
            return redirect(url_for('account_query1'))
        else:
            for key in form.errors:
                flash('Invalid '+ key,'danger')
        return render_template('query_account1.html', form = form)
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))


@app.route('/choose_transacton',methods=['GET','POST'])
def choose_transaction():
    if 'user_id' in session and session['user_type'] == 'C':
        form = TransactionForm()
        i=0
        aid_lst=[]
        aid=request.args.get('id'+str(i))
        while aid!=None:
            aid_lst.append(int(aid))
            i=i+1
            aid=request.args.get('id'+str(i))
        chcs = list(zip(aid_lst,aid_lst))
        form.account_id_choices.choices= chcs
        if form.validate_on_submit():
            print('i am here')
            button_pressed=''
            if form.deposit.data:
                button_pressed = 'deposit'
            elif form.withdraw.data:
                button_pressed = 'withdraw'
            elif form.transfer.data:
                button_pressed = 'transfer'
            return redirect(url_for(button_pressed,id=form.account_id_choices.data))
        else:
            for key in form.errors:
                flash('Invalid '+ key,'danger')
        return render_template('choose_transaction.html', form = form,title='Choose Account')
    else:
        flash('You are not logged in ','warning')
        return redirect(url_for('login'))
