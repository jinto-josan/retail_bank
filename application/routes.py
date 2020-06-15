from application import app
from flask import render_template,flash,redirect,request
from application.forms import LoginForm,RegisterForm,DataRegisterForm
import json

@app.route('/')
@app.route('/home', methods = ['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/login', methods = ['GET', 'POST'])
def login():
   form = LoginForm()
   if form.validate() == False:
      flash('All fields are required.')
   return render_template('login.html', form = form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
   form = RegisterForm()
   if form.validate() == False:
      flash('All fields are required.')
   return render_template('login.html', form = form)

@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "POST":
        req = request.form
        with open('data.json','w') as file:
            json.dump(req,file)
        return redirect("/home")
    return render_template("/dataregister.html")

@app.route('/dataregister', methods = ['GET', 'POST'])
def registerData():
   form = DataRegisterForm()
   if form.validate() == False:
       flash('All fields are required.')
   return render_template('dataregister.html', form = form)
