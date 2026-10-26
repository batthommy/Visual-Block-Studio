import pathlib
import sqlite3
from datetime import date
from functools import wraps

from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    send_from_directory,
    session,
    url_for,
)
from werkzeug import security


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

ROOT_DIR = str(pathlib.Path(__file__).parent.parent.resolve())

app = Flask(__name__, template_folder=f"{ROOT_DIR}/frontend/templates", static_folder=f"{ROOT_DIR}/frontend/static")
app.secret_key = "vbs-7f3a9c82e1b640d5a0f6c93b2e8d147a"
DATABASE = f"{ROOT_DIR}/backend/database.db"

@app.route('/project-image/<path:filename>')
def project_image(filename):
    return send_from_directory('img_project', filename)


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
    user = None

    if 'email' in session:
        con = get_db()
        con.row_factory = sqlite3.Row

        row = con.execute(
            """
            SELECT
                id, name, username, email, birthdate,
                description, created_at, friends, peoplefollowed,
                totaltime_mnt, programtime_mnt, bestlongesttime_sec
            FROM users
            WHERE email = ?
            """,
            (session['email'],)
        ).fetchone()

        if row:
            birthdate = date.fromisoformat(row['birthdate'])
            today = date.today()

            age = today.year - birthdate.year - (
                (today.month, today.day) < (birthdate.month, birthdate.day)
            )

            projects = con.execute(
                "SELECT id, name, description, created_at FROM projects WHERE owner_id = ?",
                (row['id'],)
            ).fetchall()

            user = {
                "id": row['id'],
                "name": row['name'],
                "username": row['username'],
                "email": row['email'],
                "age": age,
                "birthdate": row['birthdate'],
                "description": row['description'],
                "created_at": row['created_at'],
                "projects": [dict(project) for project in projects],
                "friends": row['friends'],
                "peoplefollowed": row['peoplefollowed'],
                "totaltime_mnt": row['totaltime_mnt'],
                "programtime_mnt": row['programtime_mnt'],
                "bestlongesttime_sec": row['bestlongesttime_sec']
            }

    con = get_db()
    con.row_factory = sqlite3.Row

    top3_rows = con.execute(
        """
        SELECT category, position, title, description, image
        FROM top3
        ORDER BY category, position
        """
    ).fetchall()

    top3 = {1: [], 2: [], 3: []}

    for project in top3_rows:
        category = project["category"]

        if category in top3:
            top3[category].append(dict(project))

    stats = {
        "active_developers": con.execute(
            "SELECT COUNT(*) FROM users"
        ).fetchone()[0],

        "completed_projects": con.execute(
            "SELECT COUNT(*) FROM projects"
        ).fetchone()[0],

        "marketplace_apps": 0
    }

    return render_template(
        "index.html",
        logged_in=user is not None,
        user=user,
        top3=top3,
        stats=stats
    )


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
                return redirect(url_for('index'))
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
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Please fill in all fields.", show_sign_up=True, Name=Name, Username=Username, Email=Email, Birthdate=Birthdate)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route('/logout', methods=['GET'])
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/mipage', methods=['GET'])
@login_required
def mipage():
    return send_from_directory(f"{ROOT_DIR}/frontend/my", "mipage.html")

app.run(debug=True)