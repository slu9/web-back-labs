from flask import Blueprint, render_template, request, make_response, redirect, url_for
import datetime
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    age = request.cookies.get('age')
    name_color = request.cookies.get('name_color')

    if not name:
        name = 'Аноним'

    if not age:
        age = 'неизвестен'

    return render_template('lab3/lab3.html',
                           name=name,
                           name_color=name_color,
                           age=age)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)

@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')

@lab3.route('/lab3/pay')
def pay():
    drink = request.args.get('drink')
    milk = 'milk' in request.args
    sugar = 'sugar' in request.args

    prices = {'coffee': 100, 'black-tea': 80, 'green-tea': 90}
    price = prices.get(drink, 0)
    if milk:
        price += 20
    if sugar:
        price += 10

    return render_template('lab3/pay.html', price=price)

@lab3.route('/lab3/settings', methods=['GET', 'POST'])
def settings():

    color  = request.values.get('color')
    bg     = request.values.get('bg')
    fs     = request.values.get('fs')
    weight = request.values.get('weight')

    if color or bg or fs or weight:
        resp = make_response(redirect(url_for('lab3.settings')))
        if color:  resp.set_cookie('color',  color)
        if bg:     resp.set_cookie('bg',     bg)
        if fs:     resp.set_cookie('fs',     fs)
        if weight: resp.set_cookie('weight', weight)
        return resp

    return render_template('lab3/settings.html',
                           color=request.cookies.get('color'),
                           bg=request.cookies.get('bg'),
                           fs=request.cookies.get('fs'),
                           weight=request.cookies.get('weight'))

@lab3.route('/lab3/clear_cookies')
def clear_cookies():
    resp = make_response(redirect(url_for('lab3.settings')))
    resp.delete_cookie('color')
    resp.delete_cookie('bg')
    resp.delete_cookie('fs')
    resp.delete_cookie('weight')
    return resp

@lab3.route('/lab3/ticket')
def ticket_form():
    errors = {}
    data = {
        'fio': request.args.get('fio', ''),
        'shelf': request.args.get('shelf', ''),
        'linen': request.args.get('linen', ''),       
        'baggage': request.args.get('baggage', ''),   
        'age': request.args.get('age', ''),
        'from_city': request.args.get('from_city', ''),
        'to_city': request.args.get('to_city', ''),
        'date': request.args.get('date', ''),
        'insurance': request.args.get('insurance', ''),
        'err': request.args.get('err', '')         
    }
    return render_template('lab3/ticket.html', data=data, errors=errors)


@lab3.route('/lab3/ticket/result')
def ticket_result():
    g = request.args
    errors = {}

    fio        = (g.get('fio') or '').strip()
    shelf      = g.get('shelf')
    linen      = g.get('linen')      
    baggage    = g.get('baggage')    
    insurance  = g.get('insurance')  
    from_city  = (g.get('from_city') or '').strip()
    to_city    = (g.get('to_city') or '').strip()
    date_trip  = g.get('date')
    age_raw    = g.get('age')

    if not fio:        errors['fio'] = 'Укажите ФИО'
    if shelf not in ('lower','upper','upper_side','lower_side'):
        errors['shelf'] = 'Выберите полку'
    if linen not in ('yes','no'):         errors['linen'] = 'Укажите про бельё'
    if baggage not in ('yes','no'):       errors['baggage'] = 'Укажите про багаж'
    if insurance not in ('yes','no'):     errors['insurance'] = 'Укажите страховку'
    if not from_city:  errors['from_city'] = 'Укажите пункт выезда'
    if not to_city:    errors['to_city'] = 'Укажите пункт назначения'
    if not date_trip:  errors['date'] = 'Укажите дату поездки'

    try:
        age = int(age_raw)
        if not (1 <= age <= 120):
            errors['age'] = 'Возраст от 1 до 120'
    except (TypeError, ValueError):
        errors['age'] = 'Введите возраст числом'

    if errors:
        return render_template('lab3/ticket.html',
                               data=g, errors=errors), 400

    price = 1000 if age >= 18 else 700
    if shelf in ('lower', 'lower_side'):
        price += 100
    if linen == 'yes':
        price += 75
    if baggage == 'yes':
        price += 250
    if insurance == 'yes':
        price += 150

    child_label = 'Детский билет' if age < 18 else ''

    return render_template('lab3/ticket_result.html',
                           fio=fio, shelf=shelf, linen=linen, baggage=baggage,
                           insurance=insurance, age=age, from_city=from_city,
                           to_city=to_city, date_trip=date_trip, price=price,
                           child_label=child_label)