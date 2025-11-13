from flask import Blueprint, render_template, request
import psycopg2

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5')
def lab():
    user = 'anonymous'
    return render_template('lab5/lab5.html', user=user)

@lab5.route('/lab5/login')
def login():
    user = 'anonymous'
    return render_template('lab5/login.html', user=user)

@lab5.route('/lab5/register', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля')

    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'sofya_zyryanova_knowledge_base',
        user = 'sofya_zyryanova_knowledge_base',
        password = 'labweb'
    )
    cur = conn.cursor()
    
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        cur.close()
        conn.close()
        return render_template('lab5/register.html', 
                               error="Такой пользователь уже существует")

    cur.execute(f"INSERT INTO users (login, password) VALUES ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)

@lab5.route('/lab5/list')
def list_articles():
    user = 'anonymous'
    return render_template('lab5/list.html', user=user)

@lab5.route('/lab5/create')
def create_article():
    user = 'anonymous'
    return render_template('lab5/create.html', user=user)
