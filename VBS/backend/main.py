# import os
import pathlib
import sqlite3
from functools import wraps

from flask import Flask, g, redirect, render_template, request, session, url_for
from werkzeug import security


@wraps
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

ROOT_DIR = str(pathlib.Path(__file__).parent.parent.resolve())

app = Flask(__name__, template_folder=f"{ROOT_DIR}/frontend/templates", static_folder=f"{ROOT_DIR}/frontend/static")
app.secret_key = "123456" #FOR DEBUG ONLY, THIS SHOULD BE CHANGED TO os.urandom(24) IN PRODUCTION

DATABASE = f"{ROOT_DIR}/backend/database.db"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db



@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        email = request.form['Email'].lower().strip()
        password = request.form['Password']
        if email and password:
            con = get_db()
            password_hased = con.execute("SELECT password FROM users WHERE email = ?", (email,)).fetchone()
            if not password_hased:
                return render_template("login.html", error="Invalid email or password", Email_log=email, Password_log=password)
            if security.check_password_hash(password_hased[0], password):
                session.clear()
                session['email'] = email
                session['username'] = con.execute("SELECT username FROM users WHERE email = ?", (email,)).fetchone()[0]
                return redirect(url_for('dashboard'))
            else:
                return render_template("login.html", error="Invalid email or password", Email_log=email, Password_log=password)
        else:
            return render_template("login.html", error="Please fill in all fields.", Email_log=email, Password_log=password)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        print(request.form)
        Name = request.form['name_signup']
        Username = request.form['username_signup'].lower().strip()
        Email = request.form['email_signup'].lower().strip()
        Password = request.form['password_signup']
        Birthdate = request.form['birth_date']
        
        if Name and Username and Email and Password and Birthdate:
            if any(char.isspace() for char in Password):
                return render_template("login.html", error="Password cannot contain whitespace", show_sign_up=True, Name=Name, Username=Username, Email=Email, Birthdate=Birthdate)
            hashed_password = security.generate_password_hash(Password)
            con = get_db()
            user_exists_em = con.execute("SELECT * FROM users WHERE email = ?", (Email,)).fetchone()
            user_exists_us = con.execute("SELECT * FROM users WHERE username = ?", (Username,)).fetchone()
            if user_exists_em or user_exists_us:
                return render_template("login.html", error="User with this email or username already exists." , show_sign_up=True, Name=Name, Username=Username, Email=Email, Birthdate=Birthdate)
            con.execute("INSERT INTO users (name, username, email, password, birthdate) VALUES (?, ?, ?, ?, ?)", (Name, Username, Email, hashed_password, Birthdate))
            con.commit()
            
            session['email'] = Email
            session['username'] = Username
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html", error="Please fill in all fields.", show_sign_up=True, Name=Name, Username=Username, Email=Email, Birthdate=Birthdate)

@login_required
@app.route('/dashboard', methods=['GET'])
def dashboard():
    return render_template("dashboard.html")

@login_required
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

app.run(debug=True)