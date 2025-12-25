import random
from flask import Blueprint, render_template, request, jsonify, session, url_for

lab9 = Blueprint('lab9', __name__)
OPENED_BOXES = set()
BOX_POSITIONS = {}
BOXES = [f"gift{i}.png" for i in range(1, 11)]

GIFTS = [
    {"msg": "С Новым годом! Пусть всё получится!", "gift": "choco.png"},
    {"msg": "Счастья, здоровья и тепла!", "gift": "toy.png"},
    {"msg": "Пусть мечты сбываются!", "gift": "cookies.png"},
    {"msg": "Удачи в учёбе и проектах!", "gift": "teddy.png"},
    {"msg": "Пусть год будет ярким!", "gift": "phonecase.png"},
    {"msg": "Больше радости каждый день!", "gift": "flowers.png"},
    {"msg": "Пусть рядом будут любимые!", "gift": "ring.png"},  
    {"msg": "Финансового роста!", "gift": "money.png"},
    {"msg": "Новых возможностей!", "gift": "book.png"},
    {"msg": "Пусть всё плохое останется в прошлом!", "gift": "star.png"},
]

def rects_intersect(a, b):
    return not (
        a["x2"] <= b["x1"] or a["x1"] >= b["x2"] or
        a["y2"] <= b["y1"] or a["y1"] >= b["y2"]
    )

def rects_intersect(a, b, pad=10):
    return not (
        a["x2"] + pad <= b["x1"] or a["x1"] >= b["x2"] + pad or
        a["y2"] + pad <= b["y1"] or a["y1"] >= b["y2"] + pad
    )

def init_positions():
    if BOX_POSITIONS:
        return

    FIELD_W = 1100
    FIELD_H = 540

    placed = []
    for i in range(10):
        for _ in range(2000):
            size = random.randint(150, 200)

            left = random.randint(0, FIELD_W - size)
            top  = random.randint(0, FIELD_H - size)

            cand = {"x1": left, "y1": top, "x2": left + size, "y2": top + size}

            if all(not rects_intersect(cand, r) for r in placed):
                placed.append(cand)
                BOX_POSITIONS[i] = {"left": left, "top": top, "size": size}
                break
        else:
            BOX_POSITIONS[i] = {"left": 20 + i * 100, "top": 20 + (i % 2) * 150, "size": 90}

@lab9.route('/lab9/')
def index():
    init_positions()
    session.setdefault('opened_count', 0)

    remaining = 10 - len(OPENED_BOXES)

    return render_template(
        'lab9/index.html',
        positions=BOX_POSITIONS,
        opened=list(OPENED_BOXES),
        opened_count=session['opened_count'],
        remaining=remaining,
        boxes=BOXES
    )

@lab9.route('/lab9/open', methods=['POST'])
def open_box():
    data = request.get_json(silent=True) or {}
    box_id = data.get('box_id', -1)

    try:
        box_id = int(box_id)
    except:
        return jsonify({"ok": False, "error": "box_id должен быть числом"}), 400

    if not (0 <= box_id <= 9):
        return jsonify({"ok": False, "error": "Некорректный box_id"}), 400

    opened_count = session.get('opened_count', 0)

    if box_id in OPENED_BOXES:
        return jsonify({
            "ok": True,
            "status": "empty",
            "opened_count": opened_count,
            "remaining": 10 - len(OPENED_BOXES)
        })

    if opened_count >= 3:
        return jsonify({
            "ok": False,
            "error": "Можно открыть не более 3 коробок",
            "opened_count": opened_count,
            "remaining": 10 - len(OPENED_BOXES)
        }), 403

    OPENED_BOXES.add(box_id)
    session['opened_count'] = opened_count + 1

    gift = GIFTS[box_id]
    gift_url = url_for('static', filename=f"lab9/{gift['gift']}")

    return jsonify({
        "ok": True,
        "status": "opened",
        "message": gift["msg"],
        "gift_url": gift_url,
        "opened_count": session['opened_count'],
        "remaining": 10 - len(OPENED_BOXES)
    })
