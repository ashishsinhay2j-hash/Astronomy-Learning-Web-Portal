# ---------------- IMPORTS ----------------
from flask import Flask, render_template, request, redirect, session, url_for, send_file
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import uuid
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "super-secret-key")
app.config["DEBUG"] = True


# ---------------- DATABASE ----------------
def get_db():
    return mysql.connector.connect(
        host=os.environ["MYSQLHOST"],
        user=os.environ["MYSQLUSER"],
        password=os.environ["MYSQLPASSWORD"],
        database=os.environ["MYSQLDATABASE"],
        port=int(os.environ["MYSQLPORT"])
    )


# ---------------- SECURITY ----------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper


def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if session.get("role") not in roles:
                return "Access Denied"
            return f(*args, **kwargs)
        return wrapper
    return decorator


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            return render_template("register.html", error="Email exists")

        cursor.execute(
            "INSERT INTO users (username,email,password,role_id) VALUES (%s,%s,%s,2)",
            (username, email, hashed)
        )
        db.commit()

        cursor.close()
        db.close()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = int(request.form.get("role"))

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            if user["role_id"] == role:
                session["user"] = user["username"]
                session["user_id"] = user["user_id"]
                session["role"] = user["role_id"]

                return redirect(
                    "/admin" if role == 1 else
                    "/teacher" if role == 3 else
                    "/dashboard"
                )

        return render_template("login.html", error="Invalid login")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("dashboard.html", courses=courses)


# ---------------- COURSE ----------------
@app.route("/course/<int:course_id>")
@login_required
def course_detail(course_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses WHERE course_id=%s", (course_id,))
    course = cursor.fetchone()

    cursor.execute("SELECT * FROM lessons WHERE course_id=%s ORDER BY position ASC", (course_id,))
    lessons = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("course_detail.html", course=course, lessons=lessons)


# ---------------- COMPLETE LESSON ----------------
@app.route("/complete/<int:lesson_id>")
@login_required
def complete(lesson_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO progress (user_id, lesson_id, status) VALUES (%s,%s,'completed')",
        (session["user_id"], lesson_id)
    )
    db.commit()

    cursor.close()
    db.close()

    return redirect(request.referrer)


# ---------------- PROGRESS ----------------
@app.route("/progress")
@login_required
def progress():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute(
        "SELECT COUNT(*) as completed FROM progress WHERE user_id=%s",
        (session["user_id"],)
    )
    completed = cursor.fetchone()["completed"]

    cursor.execute("SELECT COUNT(*) as total FROM lessons")
    total = cursor.fetchone()["total"]

    cursor.close()
    db.close()

    percentage = int((completed / total) * 100) if total > 0 else 0

    return render_template("progress.html", completed=completed, percentage=percentage)


# ---------------- CERTIFICATE ----------------
@app.route("/certificate")
@login_required
def certificate():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT username FROM users WHERE user_id=%s", (session["user_id"],))
    user = cursor.fetchone()

    cursor.execute("SELECT COUNT(*) as total FROM lessons")
    total = cursor.fetchone()["total"]

    cursor.execute(
        "SELECT COUNT(*) as completed FROM progress WHERE user_id=%s",
        (session["user_id"],)
    )
    completed = cursor.fetchone()["completed"]

    cursor.close()
    db.close()

    if completed < total:
        return render_template("certificate.html", unlocked=False)

    filename = f"certificate_{uuid.uuid4().hex}.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    elements = []
    elements.append(Paragraph("Certificate of Completion", styles["Title"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"{user['username']}", styles["Heading2"]))

    doc.build(elements)

    return send_file(filename, as_attachment=True)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)