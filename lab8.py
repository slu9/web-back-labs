from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user
from sqlalchemy import or_

lab8 = Blueprint('lab8', __name__)
from flask_login import current_user

@lab8.route('/lab8/')
def index():
    username = current_user.login if current_user.is_authenticated else 'anonymous'
    return render_template('lab8/index.html', username=username)

@lab8.route('/lab8/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember = request.form.get('remember') == '1' 

    if not login_form:
        return render_template(
            'lab8/login.html',
            error='Логин не должен быть пустым'
        )

    if not password_form:
        return render_template(
            'lab8/login.html',
            error='Пароль не должен быть пустым'
        )

    user = users.query.filter_by(login=login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            return redirect('/lab8/')
    
    return render_template(
        'lab8/login.html',
        error='Ошибка входа: логин и/или пароль неверны'
    )

@lab8.route('/lab8/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template(
            'lab8/register.html',
            error='Имя пользователя не должно быть пустым'
        )

    if not password_form:
        return render_template(
            'lab8/register.html',
            error='Пароль не должен быть пустым'
        )

    login_exists = users.query.filter_by(login=login_form).first()
    if login_exists:
        return render_template(
            'lab8/register.html',
            error='Такой пользователь уже существует'
        )

    password_hash = generate_password_hash(password_form)
    new_user = users(login=login_form, password=password_hash)
    db.session.add(new_user)
    db.session.commit()
    login_user(new_user, remember=False)

    return redirect('/lab8/')

@lab8.route('/lab8/articles/')
@login_required
def article_list():
    my_articles = articles.query.filter_by(login_id=current_user.id).order_by(articles.id.desc()).all()
    return render_template('lab8/articles.html', articles=my_articles)

@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8')

@lab8.route('/lab8/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('lab8/create.html')

    title = request.form.get('title')
    text = request.form.get('article_text')

    if not title:
        return render_template('lab8/create.html', error='Заголовок не должен быть пустым')
    if not text:
        return render_template('lab8/create.html', error='Текст статьи не должен быть пустым')

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=text,
        is_favorite=False,
        is_public=False,
        likes=0
    )

    is_public = request.form.get('is_public') == '1'

    new_article = articles(
        login_id=current_user.id,
        title=title,
        article_text=text,
        is_public=is_public
    )

    db.session.add(new_article)
    db.session.commit()

    return redirect('/lab8/articles/')

@lab8.route('/lab8/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    art = articles.query.get_or_404(article_id)

    if art.login_id != current_user.id:
        return "Доступ запрещён", 403

    if request.method == 'GET':
        return render_template('lab8/edit.html', article=art)

    title = request.form.get('title')
    text = request.form.get('article_text')

    if not title:
        return render_template('lab8/edit.html', article=art, error='Заголовок не должен быть пустым')
    if not text:
        return render_template('lab8/edit.html', article=art, error='Текст статьи не должен быть пустым')

    art.title = title
    art.article_text = text
    db.session.commit()

    return redirect('/lab8/articles/')

@lab8.route('/lab8/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    art = articles.query.get_or_404(article_id)

    if art.login_id != current_user.id:
        return "Доступ запрещён", 403

    db.session.delete(art)
    db.session.commit()

    return redirect('/lab8/articles/')

@lab8.route('/lab8/public/')
def public_articles():
    pub = articles.query.filter_by(is_public=True).order_by(articles.id.desc()).all()
    return render_template('lab8/public.html', articles=pub)

@lab8.route('/lab8/search')
def search():
    q = (request.args.get('q') or '').strip()

    results = []
    if q:
        pattern = f"%{q}%"

        cond_public = articles.is_public.is_(True)

        if current_user.is_authenticated:
            cond_owner = (articles.login_id == current_user.id)
            base_cond = or_(cond_public, cond_owner)
        else:
            base_cond = cond_public

        results = (articles.query
                   .filter(base_cond)
                   .filter(or_(articles.title.ilike(pattern),
                               articles.article_text.ilike(pattern)))
                   .order_by(articles.id.desc())
                   .all())

    return render_template('lab8/search.html', q=q, articles=results)