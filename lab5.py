from flask import Blueprint, render_template, request, session, redirect, current_app, url_for
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'sofya_zyryanova_knowledge_base',
            user = 'sofya_zyryanova_knowledge_base',
            password = 'labweb'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        bd_path = path.join(dir_path, "database.bd")
        conn = sqlite3.connect(bd_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@lab5.route('/lab5/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')

    login_val = request.form.get('login', '').strip()
    real_name = request.form.get('real_name', '').strip()
    password  = request.form.get('password', '').strip()

    if not (login_val and password):
        return render_template(
            'lab5/register.html',
            error='Заполните логин и пароль',
            login=login_val,
            real_name=real_name
        )

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login FROM users WHERE login=%s;", (login_val,))
    else:
        cur.execute("SELECT login FROM users WHERE login=?;", (login_val,))
    if cur.fetchone():
        db_close(conn, cur)
        return render_template(
            'lab5/register.html',
            error="Такой пользователь уже существует",
            login=login_val,
            real_name=real_name
        )

    password_hash = generate_password_hash(password)

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO users (login, real_name, password) VALUES (%s, %s, %s);",
            (login_val, real_name, password_hash)
        )
    else:
        cur.execute(
            "INSERT INTO users (login, real_name, password) VALUES (?, ?, ?);",
            (login_val, real_name, password_hash)
        )

    db_close(conn, cur)

    return render_template('lab5/success.html',
                           login=login_val,
                           real_name=real_name)

@lab5.route('/lab5/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login_val = request.form.get('login', '').strip()
    password  = request.form.get('password', '').strip()

    if not (login_val and password):
        return render_template('lab5/login.html', error="Заполните поля")
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login_val,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login_val,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')
    

    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html',
                               error='Логин и/или пароль неверны')

    session['login'] = user['login']
    session['real_name'] = user.get('real_name') if isinstance(user, dict) else user['real_name']

    db_close(conn, cur)

    return render_template(
        'lab5/success_login.html',
        login=user['login'],
        real_name=session.get('real_name')
    )

@lab5.route('/lab5/create', methods = ['GET', 'POST'])
def create():
    login=session.get('login')
    if not login:
        return redirect('/lab5/login')
    
    if request.method == 'GET':
        return render_template('lab5/create_article.html')
    
    title = request.form.get('title')
    article_text = request.form.get('article_text')
    is_favorite = 1 if request.form.get('is_favorite') else 0  
    is_public = 1 if request.form.get('is_public') else 0

    if not title or not article_text:
        return render_template(
            'lab5/create_article.html',
            error='Название и текст статьи не должны быть пустыми.',
            title=title,
            article_text=article_text
        )
    
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user_id = cur.fetchone()["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) "
            "VALUES (%s, %s, %s, %s, %s);",
            (user_id, title, article_text, bool(is_favorite), bool(is_public))
        )
    else:
        cur.execute(
            "INSERT INTO articles (user_id, title, article_text, is_favorite, is_public) "
            "VALUES (?, ?, ?, ?, ?);",
            (user_id, title, article_text, is_favorite, is_public)
        )

    db_close(conn, cur)
    return redirect('/lab5')

@lab5.route('/lab5/list')
def list_articles():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    row = cur.fetchone()

    if not row:
        db_close(conn, cur)
        return render_template('lab5/articles.html', articles=[], login=login)

    user_id = row["id"]
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT * FROM articles WHERE user_id=%s ORDER BY is_favorite DESC, id DESC;",
            (user_id,)
        )
    else:
        cur.execute(
            "SELECT * FROM articles WHERE user_id=? ORDER BY is_favorite DESC, id DESC;",
            (user_id,)
        )

    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/articles.html', articles=articles, login=login)
    
@lab5.route('/lab5/edit/<int:article_id>', methods=['GET', 'POST'])
def edit_article(article_id):
    login = session.get('login')
    if not login:
        return redirect('/lab5/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    row = cur.fetchone()

    if not row:
        db_close(conn, cur)
        return redirect('/lab5/list')
    user_id = row["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM articles WHERE id=%s AND user_id=%s;",
                    (article_id, user_id))
    else:
        cur.execute("SELECT * FROM articles WHERE id=? AND user_id=?;",
                    (article_id, user_id))
    article = cur.fetchone()

    if not article:
        db_close(conn, cur)
        return render_template('lab5/articles.html', articles=[], login=login)

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template('lab5/edit_article.html', article=article)

    title = request.form.get('title', '').strip()
    article_text = request.form.get('article_text', '').strip()
    is_favorite = 1 if request.form.get('is_favorite') else 0
    is_public   = 1 if request.form.get('is_public') else 0

    if not title or not article_text:
        db_close(conn, cur)
        return render_template(
            'lab5/edit_article.html',
            article=article,
            error='Название и текст статьи не должны быть пустыми.'
        )

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "UPDATE articles SET title=%s, article_text=%s WHERE id=%s AND user_id=%s;",
            (title, article_text, article_id, user_id)
        )
    else:
        cur.execute(
            "UPDATE articles SET title=?, article_text=? WHERE id=? AND user_id=?;",
            (title, article_text, article_id, user_id)
        )

    db_close(conn, cur)
    return redirect('/lab5/list')

@lab5.route('/lab5/delete/<int:article_id>', methods=['POST'])
def delete_article(article_id):
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()
    
    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT id FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT id FROM users WHERE login=?;", (login,))
    row = cur.fetchone()

    if not row:
        db_close(conn, cur)
        return redirect(url_for('lab5.list_articles'))

    user_id = row["id"]

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "DELETE FROM articles WHERE id=%s AND user_id=%s;",
            (article_id, user_id)
        )
    else:
        cur.execute(
            "DELETE FROM articles WHERE id=? AND user_id=?;",
            (article_id, user_id)
        )

    db_close(conn, cur)
    return redirect(url_for('lab5.list_articles'))

@lab5.route('/lab5/logout')
def logout():
    session.pop('login', None)
    return redirect('/lab5')

@lab5.route('/lab5/users')
def users_list():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")
    else:
        cur.execute("SELECT login, real_name FROM users ORDER BY login;")

    users = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/users.html', users=users)

@lab5.route('/lab5/profile', methods=['GET', 'POST'])
def profile():
    login = session.get('login')
    if not login:
        return redirect(url_for('lab5.login'))

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users WHERE login=%s;", (login,))
    else:
        cur.execute("SELECT * FROM users WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return redirect(url_for('lab5.login'))

    if request.method == 'GET':
        db_close(conn, cur)
        return render_template(
            'lab5/profile.html',
            login=login,
            real_name=user['real_name']
        )

    new_name = request.form.get('real_name', '').strip()
    new_pass = request.form.get('password', '').strip()
    confirm  = request.form.get('confirm', '').strip()

    if not new_name:
        db_close(conn, cur)
        return render_template(
            'lab5/profile.html',
            login=login,
            real_name=user['real_name'],
            error="Имя не должно быть пустым"
        )

    if new_pass or confirm:
        if new_pass != confirm:
            db_close(conn, cur)
            return render_template(
                'lab5/profile.html',
                login=login,
                real_name=new_name,
                error="Пароль и подтверждение должны совпадать"
            )
        new_pass_hash = generate_password_hash(new_pass)
    else:
        new_pass_hash = None

    if current_app.config['DB_TYPE'] == 'postgres':
        if new_pass_hash:
            cur.execute(
                "UPDATE users SET real_name=%s, password=%s WHERE login=%s;",
                (new_name, new_pass_hash, login)
            )
        else:
            cur.execute(
                "UPDATE users SET real_name=%s WHERE login=%s;",
                (new_name, login)
            )
    else:
        if new_pass_hash:
            cur.execute(
                "UPDATE users SET real_name=?, password=? WHERE login=?;",
                (new_name, new_pass_hash, login)
            )
        else:
            cur.execute(
                "UPDATE users SET real_name=? WHERE login=?;",
                (new_name, login)
            )

    db_close(conn, cur)
    session['real_name'] = new_name

    return redirect(url_for('lab5.profile'))

@lab5.route('/lab5/public')
def public_articles():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute(
            "SELECT a.title, a.article_text, a.is_favorite, u.login, u.real_name "
            "FROM articles a "
            "JOIN users u ON a.user_id = u.id "
            "WHERE a.is_public = TRUE "
            "ORDER BY a.is_favorite DESC, a.id DESC;"
        )
    else:
        cur.execute(
            "SELECT a.title, a.article_text, a.is_favorite, u.login, u.real_name "
            "FROM articles a "
            "JOIN users u ON a.user_id = u.id "
            "WHERE a.is_public = 1 "
            "ORDER BY a.is_favorite DESC, a.id DESC;"
        )

    articles = cur.fetchall()
    db_close(conn, cur)

    return render_template('lab5/public_articles.html', articles=articles)
