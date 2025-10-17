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

PRODUCTS = [
    {"name": "iPhone 13",         "price": 56000, "brand": "Apple",  "color": "blue"},
    {"name": "iPhone 14",         "price": 72000, "brand": "Apple",  "color": "midnight"},
    {"name": "iPhone 15",         "price": 89000, "brand": "Apple",  "color": "pink"},
    {"name": "Galaxy S21",        "price": 45000, "brand": "Samsung","color": "gray"},
    {"name": "Galaxy S22",        "price": 62000, "brand": "Samsung","color": "black"},
    {"name": "Galaxy S23",        "price": 78000, "brand": "Samsung","color": "green"},
    {"name": "Pixel 6",           "price": 38000, "brand": "Google", "color": "black"},
    {"name": "Pixel 7",           "price": 52000, "brand": "Google", "color": "snow"},
    {"name": "Pixel 8",           "price": 67000, "brand": "Google", "color": "hazel"},
    {"name": "Redmi Note 12",     "price": 19000, "brand": "Xiaomi", "color": "blue"},
    {"name": "Redmi Note 13",     "price": 23000, "brand": "Xiaomi", "color": "black"},
    {"name": "Mi 12",             "price": 41000, "brand": "Xiaomi", "color": "purple"},
    {"name": "OnePlus 10T",       "price": 39000, "brand": "OnePlus","color": "jade"},
    {"name": "OnePlus 11",        "price": 56000, "brand": "OnePlus","color": "black"},
    {"name": "Honor 90",          "price": 32000, "brand": "Honor",  "color": "blue"},
    {"name": "Honor Magic 6",     "price": 73000, "brand": "Honor",  "color": "black"},
    {"name": "Huawei P50",        "price": 47000, "brand": "Huawei", "color": "gold"},
    {"name": "Huawei P60",        "price": 64000, "brand": "Huawei", "color": "black"},
    {"name": "Realme 11 Pro",     "price": 28000, "brand": "Realme", "color": "green"},
    {"name": "Realme GT Neo 3",   "price": 34000, "brand": "Realme", "color": "blue"},
    {"name": "Moto G84",          "price": 21000, "brand": "Motorola","color": "magenta"},
    {"name": "Moto Edge 40",      "price": 36000, "brand": "Motorola","color": "black"},
]

@lab3.route('/lab3/products')
def products():

    min_all = min(p["price"] for p in PRODUCTS)
    max_all = max(p["price"] for p in PRODUCTS)

    g = request.args

    if g.get('reset'):
        resp = make_response(redirect(url_for('lab3.products')))
        resp.delete_cookie('price_min')
        resp.delete_cookie('price_max')
        return resp

    qmin = g.get('min')
    qmax = g.get('max')
    if (qmin is None and qmax is None):
        qmin = request.cookies.get('price_min')
        qmax = request.cookies.get('price_max')

    def to_int(x):
        try:
            return int(x) if x not in (None, '',) else None
        except ValueError:
            return None

    vmin = to_int(qmin)
    vmax = to_int(qmax)

    if vmin is not None and vmax is not None and vmin > vmax:
        vmin, vmax = vmax, vmin

    items = PRODUCTS
    if vmin is not None:
        items = [p for p in items if p["price"] >= vmin]
    if vmax is not None:
        items = [p for p in items if p["price"] <= vmax]

    count = len(items)

    if ('min' in g) or ('max' in g):
        resp = make_response(render_template(
            'lab3/products.html',
            products=items,
            count=count,
            min_all=min_all,
            max_all=max_all,
            cur_min=vmin,
            cur_max=vmax
        ))
        if vmin is None:
            resp.delete_cookie('price_min')
        else:
            resp.set_cookie('price_min', str(vmin))
        if vmax is None:
            resp.delete_cookie('price_max')
        else:
            resp.set_cookie('price_max', str(vmax))
        return resp

    return render_template(
        'lab3/products.html',
        products=items,
        count=count,
        min_all=min_all,
        max_all=max_all,
        cur_min=vmin,
        cur_max=vmax
    )