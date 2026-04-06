
from flask import Flask, render_template, request, redirect, session, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
import uuid

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "super-secret-key")
app.config["DEBUG"] = True

# ---------------- DATABASE ----------------
def get_db():
    return mysql.connector.connect(
        host=os.environ["MYSQLHOST"],   # ❗ no default
        user=os.environ["MYSQLUSER"],
        password=os.environ["MYSQLPASSWORD"],
        database=os.environ["MYSQLDATABASE"],
        port=int(os.environ["MYSQLPORT"])
    )



# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- SECURITY ----------------
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
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

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            return render_template("register.html", error="Email already exists")

        cursor.execute(
            "INSERT INTO users (username, email, password, role_id) VALUES (%s,%s,%s,2)",
            (username, email, password)
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
        role = request.form.get("role")

        # ✅ prevent crash
        if not email or not password or not role:
            return render_template("login.html", error="All fields required")

        selected_role = int(role)

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user["password"], password):
            if user["role_id"] == selected_role:
                session["user"] = user["username"]
                session["user_id"] = user["user_id"]
                session["role"] = user["role_id"]

                return redirect(
                    "/admin" if user["role_id"] == 1
                    else "/teacher" if user["role_id"] == 3
                    else "/dashboard"
                )
            else:
                return render_template("login.html", error="Wrong role selected")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")

# ---------------- FORGOT PASSWORD ----------------
@app.route("/forgot", methods=["GET","POST"])
def forgot():
    if request.method == "POST":
        email = request.form["email"]
        token = str(uuid.uuid4())

        db = get_db()
        cursor = db.cursor()

        cursor.execute("UPDATE users SET reset_token=%s WHERE email=%s", (token, email))
        db.commit()

        cursor.close()
        db.close()

        return f"Reset link: /reset/{token}"

    return render_template("forgot.html")

# ---------------- RESET PASSWORD ----------------
@app.route("/reset/<token>", methods=["GET","POST"])
def reset(token):
    if request.method == "POST":
        new_password = generate_password_hash(request.form["password"])

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "UPDATE users SET password=%s WHERE reset_token=%s",
            (new_password, token)
        )
        db.commit()

        cursor.close()
        db.close()

        return redirect("/login")

    return render_template("reset.html")

# ---------------- PANELS ----------------
@app.route("/admin")
@login_required
@roles_required(1)
def admin():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("admin.html", users=users)

@app.route("/teacher")
@login_required
@roles_required(3)
def teacher():
    return render_template("teacher.html")

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
#----------------- COURSE ----------------
@app.route("/course/<int:course_id>")
@login_required
def course_detail(course_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # get topics
    cursor.execute("SELECT * FROM topics WHERE course_id=%s", (course_id,))
    topics = cursor.fetchall()

    # get lessons inside each topic
    for t in topics:
        cursor.execute("SELECT * FROM lessons WHERE topic_id=%s", (t["topic_id"],))
        t["lessons"] = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("course.html", topics=topics)
#----------------course route ----------------
@app.route("/courses")
@login_required
def courses():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("courses.html", courses=courses)
#----------------- Courses ----------------
@app.route("/course/<int:course_id>")
@login_required
def course_detail(course_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM topics WHERE course_id=%s", (course_id,))
    topics = cursor.fetchall()

    for t in topics:
        cursor.execute("SELECT * FROM lessons WHERE topic_id=%s", (t["topic_id"],))
        t["lessons"] = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("course.html", topics=topics)
#----------------- QUIZ----------------
@app.route("/quiz/<int:quiz_id>", methods=["GET","POST"])
@login_required
def quiz(quiz_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Get questions
    cursor.execute("SELECT * FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cursor.fetchall()

    for q in questions:
        cursor.execute("SELECT * FROM options WHERE question_id=%s", (q["question_id"],))
        q["options"] = cursor.fetchall()

    if request.method == "POST":
        score = 0
        total = len(questions)

        # Create attempt
        cursor.execute(
            "INSERT INTO quiz_attempts (user_id, quiz_id, score, total) VALUES (%s,%s,0,%s)",
            (session["user_id"], quiz_id, total)
        )
        db.commit()

        attempt_id = cursor.lastrowid

        # Check answers
        for q in questions:
            selected = request.form.get(f"q{q['question_id']}")

            if selected:
                cursor.execute("SELECT * FROM options WHERE option_id=%s", (selected,))
                opt = cursor.fetchone()

                if opt and opt["is_correct"]:
                    score += 1

                # Save answer
                cursor.execute(
                    "INSERT INTO user_answers (attempt_id, question_id, selected_option) VALUES (%s,%s,%s)",
                    (attempt_id, q["question_id"], selected)
                )

        # Update score
        cursor.execute(
            "UPDATE quiz_attempts SET score=%s WHERE attempt_id=%s",
            (score, attempt_id)
        )
        db.commit()

        cursor.close()
        db.close()

        return render_template("result.html", score=score, total=total)

    cursor.close()
    db.close()

    return render_template("quiz.html", questions=questions, quiz_id=quiz_id)

# ---------------- CERTIFICATE ----------------
@app.route("/certificate")
@login_required
def certificate():
    filename = f"Cert_{session['user_id']}_{uuid.uuid4().hex[:6]}.pdf"
    return f"Certificate generated: {filename}"
#---------------- Leaderboard ----------------
@app.route("/leaderboard")
@login_required
def leaderboard():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT users.username, SUM(quiz_attempts.score) AS total_score
        FROM quiz_attempts
        JOIN users ON users.user_id = quiz_attempts.user_id
        GROUP BY users.user_id
        ORDER BY total_score DESC
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("leaderboard.html", data=data)
# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))