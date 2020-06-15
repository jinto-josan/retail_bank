'''
To define all the routes
'''
from application import app
from flask import render_template,flash,redirect,request

@app.route('/')
@app.route('/login', methods = ['GET', 'POST'])
def login():
    return '<h1>login page</h1>'
