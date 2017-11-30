import string
import random
from flask import Flask
from flask import render_template
from flask import g, request, redirect, url_for
from flask import session
from flask_cors import CORS, cross_origin
from functools import wraps
from api import *

app = Flask(__name__)
CORS(app)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect("login")
        return f(*args, **kwargs)
    return decorated_function

def step1_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "step1" not in session:
            return redirect("login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/api/send", methods=["GET", "POST"])
@app.route("/api/send/<string:message>", methods=["GET", "POST"])
def handle_message(message=None):
    return jsonify({
                    "intent":intent["intent"],
                    "score":intent["score"],
                    "text": not_classified,
                    "accurate": False
            })

@app.route('/login', methods = ['GET', 'POST'])
def startpage():
    if request.form:
        name = request.form["name"]
        surname = request.form["surname"]
        if check_name(name) and check_surname(surname):
            session["step1"] = True
            session["surname"] = surname
            session["user_id"] = get_id(surname)
            return redirect("login/2")
        else:
            error = "Falsche Benutzerdaten"
            return render_template("login.html", error=error, css_class="error")
    return render_template("login.html")

@app.route("/login/2", methods=["GET", "POST"])
@step1_required
def phone():
    if request.form:
        phonenumber = request.form["phonenumber"]
        if check_phonenumber(session["surname"], phonenumber):
            session["user"] = session["user_id"]
            return redirect("chat")
        error = "Falsche Telefonnummer"
        return render_template("phonenumber.html", error=error, css_class="error")
    return render_template("phonenumber.html")

@app.route("/chat")
@login_required
def chat():
    return render_template("chat.html")


if __name__ == '__main__':
    app.secret_key = "".join([random.choice(string.hexdigits) for i in range(30)])
    app.run(debug=True, threaded=True)