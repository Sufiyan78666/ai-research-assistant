import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import (
    LoginManager, UserMixin, login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from db import get_conn


# Load env vars
load_dotenv()

# Flask app with absolute template/static paths (project root level)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app = Flask(
    __name__,
    static_folder=os.path.join(BASE_DIR, "static"),
    template_folder=os.path.join(BASE_DIR, "templates"),
)
app.secret_key = os.getenv("SECRET_KEY", "dev_key")

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# --- User model wrapper for Flask-Login ---
class User(UserMixin):
    def __init__(self, id, username, email, password_hash):
        self.id = str(id)
        self.username = username
        self.email = email
        self.password_hash = password_hash

def _get_user_by_id(user_id):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE id=%s", (user_id,))
        row = cur.fetchone()
        return User(row["id"], row["username"], row["email"], row["password_hash"]) if row else None
    finally:
        conn.close()

def _get_user_by_username(username):
    conn = get_conn()
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        row = cur.fetchone()
        return User(row["id"], row["username"], row["email"], row["password_hash"]) if row else None
    finally:
        conn.close()

@login_manager.user_loader
def load_user(user_id):
    return _get_user_by_id(user_id)

# ---------------- Routes -----------------
@app.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    return redirect(url_for("index"))

@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        hashed_pw = generate_password_hash(password)

        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
                        (username, email, hashed_pw))
            conn.commit()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except Exception as e:
            flash("Error: " + str(e), "danger")
        finally:
            conn.close()
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = _get_user_by_username(username)
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard"))
        else:
            flash("Invalid username or password", "danger")
    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_conn()
    abstracts = []
    try:
        cur = conn.cursor(dictionary=True)
        cur.execute(
            "SELECT title, content, created_at FROM abstracts WHERE user_id=%s ORDER BY created_at DESC",
            (current_user.id,)
        )
        abstracts = cur.fetchall()
    finally:
        conn.close()
    return render_template("dashboard.html", username=current_user.username, abstracts=abstracts)

@app.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")
        if not content:
            flash("Abstract content is required.", "danger")
            return redirect(url_for("dashboard"))
        conn = get_conn()
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO abstracts (user_id, title, content) VALUES (%s, %s, %s)",
                (current_user.id, title, content)
            )
            conn.commit()
            flash("Abstract uploaded successfully.", "success")
        except Exception as e:
            flash("Error: " + str(e), "danger")
        finally:
            conn.close()
        return redirect(url_for("dashboard"))
    # For GET, redirect to dashboard where the form exists
    return redirect(url_for("dashboard"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    host = os.getenv("FLASK_HOST", "0.0.0.0")
    port = int(os.getenv("FLASK_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "true").lower() == "true"
    app.run(debug=debug, host=host, port=port)
