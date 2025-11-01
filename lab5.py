from flask import Blueprint, render_template

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5')
def lab():
    user = 'anonymous'
    return render_template('lab5/lab5.html', user=user)

@lab5.route('/lab5/login')
def login():
    user = 'anonymous'
    return render_template('lab5/login.html', user=user)

@lab5.route('/lab5/register')
def register():
    user = 'anonymous'
    return render_template('lab5/register.html', user=user)

@lab5.route('/lab5/list')
def list_articles():
    user = 'anonymous'
    return render_template('lab5/list.html', user=user)

@lab5.route('/lab5/create')
def create_article():
    user = 'anonymous'
    return render_template('lab5/create.html', user=user)
