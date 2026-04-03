from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "secret"

db = mysql.connector.connect(
    host="localhost",
    user="astro_user",
    password="1234",
    database="astronomy_platform"
)

cursor = db.cursor(dictionary=True)

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

        # check duplicate
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
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cursor.fetchone()

        if not user:
            return "User not found"

        if user["password"] != password:
            return "Wrong password"

        # ✅ set session AFTER login
        session["user"] = user["username"]
        session["user_id"] = user["user_id"]
        session["role"] = user["role_id"]

        print("LOGGED IN:", user["username"], "ROLE:", user["role_id"])

        return redirect("/dashboard")

    return render_template("login.html")

# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if not session.get("user"):
        return redirect("/login")

    return render_template("dashboard.html")

# ---------------- Admin Dashboard ----------------
@app.route("/admin")
def admin():
    if session.get("role") != 1:
        return "Access Denied"

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    return render_template("admin.html", users=users)

# ---------------- Add TOPICS ----------------
@app.route("/add_topic", methods=["GET", "POST"])
def add_topic():
    if session.get("role") != 1:
        return "Access Denied"

    if request.method == "POST":
        topic_name = request.form["topic_name"]

        cursor.execute("INSERT INTO topics (topic_name) VALUES (%s)", (topic_name,))
        db.commit()

        return "Topic Added"

    return render_template("add_topic.html")

#-------------------Courses----------------------
@app.route("/courses")
def courses():
    if not session.get("user"):
        return redirect("/login")

    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    return render_template("courses.html", courses=courses)

#---------------- Lesson Complete ----------------
@app.route("/complete/<int:lesson_id>")
def complete_lesson(lesson_id):
    if not session.get("user"):
        return redirect("/login")

    cursor.execute(
        "INSERT INTO progress (user_id, lesson_id, status) VALUES (%s,%s,'completed')",
        (session["user_id"], lesson_id))
    cursor.execute(
    "SELECT * FROM progress WHERE user_id=%s AND lesson_id=%s",
    (session["user_id"], lesson_id)
)
 
    db.commit()

    return "Lesson Completed"

#---------------- Progress ----------------
@app.route("/progress")
def progress():
    if not session.get("user"):
        return redirect("/login")

    user_id = session["user_id"]

    # get attempts
    cursor.execute("SELECT * FROM quiz_attempts WHERE user_id=%s", (user_id,))
    attempts = cursor.fetchall()

    total_attempts = len(attempts)

    best_score = 0
    total_score = 0

    for a in attempts:
        total_score += a["score"]
        if a["score"] > best_score:
            best_score = a["score"]

    average_score = total_score / total_attempts if total_attempts > 0 else 0

    # completed lessons
    cursor.execute("SELECT COUNT(*) as total FROM progress WHERE user_id=%s", (user_id,))
    completed = cursor.fetchone()["total"]

    return render_template(
        "progress.html",
        total_attempts=total_attempts,
        best_score=best_score,
        average_score=round(average_score, 2),
        completed=completed
    )

#---------------- Leaderboard ----------------
@app.route("/leaderboard")
def leaderboard():
    if not session.get("user"):
        return redirect("/login")

    cursor.execute("""
        SELECT users.username, SUM(quiz_attempts.score) AS total_score
        FROM quiz_attempts
        JOIN users ON users.user_id = quiz_attempts.user_id
        GROUP BY users.user_id
        ORDER BY total_score DESC
    """)

    data = cursor.fetchall()

    return render_template("leaderboard.html", data=data)

#---------------- Certificate ----------------
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

    # get questions
    cursor.execute("SELECT * FROM questions WHERE quiz_id=%s", (quiz_id,))
    questions = cursor.fetchall()

    for q in questions:
        cursor.execute("SELECT * FROM options WHERE question_id=%s", (q["question_id"],))
        q["options"] = cursor.fetchall()

    if request.method == "POST":
        score = 0
        total = len(questions)

        # create attempt
        cursor.execute(
            "INSERT INTO quiz_attempts (user_id,quiz_id,score,total) VALUES (%s,%s,0,%s)",
            (session["user_id"], quiz_id, total)
        )
        db.commit()

        attempt_id = cursor.lastrowid

        # loop answers
        for q in questions:
            selected = request.form.get(f"q{q['question_id']}")

            if selected:
                cursor.execute(
                    "SELECT * FROM options WHERE option_id=%s",
                    (selected,)
                )
                opt = cursor.fetchone()

                if opt and opt["is_correct"]:
                    score += 1

                # save answer
                cursor.execute(
                    "INSERT INTO user_answers (attempt_id,question_id,selected_option) VALUES (%s,%s,%s)",
                    (attempt_id, q["question_id"], selected)
                )

        # update score
        cursor.execute(
            "UPDATE quiz_attempts SET score=%s WHERE attempt_id=%s",
            (score, attempt_id)
        )
        db.commit()

        return render_template("result.html", score=score, total=total)

    return render_template("quiz.html", questions=questions)




# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)