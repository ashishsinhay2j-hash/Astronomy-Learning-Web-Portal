
from flask import Flask, render_template, request, redirect, session
import mysql.connector
import os

app = Flask(__name__)
app.secret_key = "secret"
app.config["DEBUG"] = True

# ---------------- DB CONNECTION ----------------
def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 3306)),
        ssl_disabled=False
    )
    

@app.route("/testdb")
def testdb():
    try:
        db = get_db()
        return "DB Connected ✅"
    except Exception as e:
        return str(e)
# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("index.html")

# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (username, email))
        if cursor.fetchone():
            return "User already exists"

        cursor.execute(
            "INSERT INTO users (username,email,password,role_id) VALUES (%s,%s,%s,2)",
            (username, email, password)
        )
        db.commit()

        return redirect("/login")

    return render_template("register.html")

# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET","POST"])
def login():
    try:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            db = get_db()
            cursor = db.cursor(dictionary=True)

            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()

            if not user:
                return "User not found"

            if user["password"] != password:
                return "Wrong password"

            session["user"] = user["username"]
            session["user_id"] = user["user_id"]
            session["role"] = user["role_id"]

            return redirect("/dashboard")

        return render_template("login.html")

    except Exception as e:
        return str(e)

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/login")
    return render_template("dashboard.html")

# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():
    if session.get("role") != 1:
        return "Access Denied"

    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template("admin.html", users=users)

# ---------------- ADD TOPIC ----------------
@app.route("/add_topic", methods=["GET", "POST"])
def add_topic():
    if session.get("role") != 1:
        return "Access Denied"

    if request.method == "POST":
        topic_name = request.form["topic_name"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute("INSERT INTO topics (topic_name) VALUES (%s)", (topic_name,))
        db.commit()

        return "Topic Added"

    return render_template("add_topic.html")

# ---------------- COURSES ----------------
@app.route("/courses")
def courses():
    if not session.get("user"):
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    return render_template("courses.html", courses=courses)

# ---------------- COMPLETE LESSON ----------------
@app.route("/complete/<int:lesson_id>")
def complete_lesson(lesson_id):
    if not session.get("user"):
        return redirect("/login")

    db = get_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO progress (user_id, lesson_id, status) VALUES (%s,%s,'completed')",
        (session["user_id"], lesson_id)
    )

    db.commit()
    return "Lesson Completed"

# ---------------- PROGRESS ----------------
@app.route("/progress")
def progress():
    if not session.get("user"):
        return redirect("/login")

    user_id = session["user_id"]

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM quiz_attempts WHERE user_id=%s", (user_id,))
    attempts = cursor.fetchall()

    total_attempts = len(attempts)
    best_score = max([a["score"] for a in attempts], default=0)
    total_score = sum([a["score"] for a in attempts])
    average_score = total_score / total_attempts if total_attempts else 0

    cursor.execute("SELECT COUNT(*) as total FROM progress WHERE user_id=%s", (user_id,))
    completed = cursor.fetchone()["total"]

    return render_template(
        "progress.html",
        total_attempts=total_attempts,
        best_score=best_score,
        average_score=round(average_score, 2),
        completed=completed
    )

# ---------------- LEADERBOARD ----------------
@app.route("/leaderboard")
def leaderboard():
    if not session.get("user"):
        return redirect("/login")

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

    return render_template("leaderboard.html", data=data)

# ---------------- CERTIFICATE ----------------
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

@app.route("/certificate")
def certificate():
    if not session.get("user"):
        return redirect("/login")

    filename = f"{session['user']}_certificate.pdf"

    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("Certificate of Completion", styles["Title"]))
    content.append(Paragraph(f"This is to certify that {session['user']} has completed the course.", styles["Normal"]))

    doc.build(content)

    return f"Certificate generated: {filename}"

# ---------------- QUIZ ----------------
@app.route("/quiz/<int:quiz_id>", methods=["GET","POST"])
def quiz(quiz_id):
    if not session.get("user"):
        return redirect("/login")

    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT * FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cursor.fetchall()

    for q in questions:
        cursor.execute("SELECT * FROM options WHERE question_id=%s", (q["question_id"],))
        q["options"] = cursor.fetchall()

    if request.method == "POST":
        score = 0
        total = len(questions)

        cursor.execute(
            "INSERT INTO quiz_attempts (user_id,quiz_id,score,total) VALUES (%s,%s,0,%s)",
            (session["user_id"], quiz_id, total)
        )
        db.commit()

        attempt_id = cursor.lastrowid

        for q in questions:
            selected = request.form.get(f"q{q['question_id']}")

            if selected:
                cursor.execute("SELECT * FROM options WHERE option_id=%s", (selected,))
                opt = cursor.fetchone()

                if opt and opt["is_correct"]:
                    score += 1

                cursor.execute(
                    "INSERT INTO user_answers (attempt_id,question_id,selected_option) VALUES (%s,%s,%s)",
                    (attempt_id, q["question_id"], selected)
                )

        cursor.execute(
            "UPDATE quiz_attempts SET score=%s WHERE attempt_id=%s",
            (score, attempt_id)
        )
        db.commit()

        return render_template("result.html", score=score, total=total)

    # ✅ IMPORTANT FIX HERE
    return render_template("quiz.html", questions=questions, quiz_id=quiz_id)

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

