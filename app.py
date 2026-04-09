from flask import send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
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
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        if not username or not email or not password:
            return render_template("register.html", error="All fields required")

        hashed = generate_password_hash(password)

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        if cursor.fetchone():
            return render_template("register.html", error="Email already exists")

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
        role = request.form.get("role")

        if not email or not password:
          return render_template("login.html", error="Email and password required")

        if not role:
          return render_template("login.html", error="Please select a role")
          
        selected_role = int(role)

        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT * FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()

        if user:
            # support both hashed + plain password
             if check_password_hash(user["password"], password):

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

        return render_template("login.html", error="Invalid email or password")

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

        return render_template("forgot.html", link=f"/reset/{token}")

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
#------------Delete----------------
@app.route("/delete_account")
@login_required
def delete_account():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE user_id=%s", (session["user_id"],))
    db.commit()

    cursor.close()
    db.close()

    session.clear()

    return redirect("/")
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

#----------------- ADMIN REPORT ----------------
@app.route("/admin_report")
@login_required
@roles_required(1)
def admin_report():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("SELECT username, email, role_id FROM users")
    users = cursor.fetchall()

    cursor.close()
    db.close()

    filename = "admin_report.pdf"
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Admin Report - Users", styles["Title"]))
    elements.append(Spacer(1, 20))

    for u in users:
        text = f"Name: {u['username']} | Email: {u['email']} | Role: {u['role_id']}"
        elements.append(Paragraph(text, styles["Normal"]))
        elements.append(Spacer(1, 10))

    doc.build(elements)

    from flask import send_file

    return send_file(filename, as_attachment=True)
#----------------- TEACHER ----------------
@app.route("/teacher")
@login_required
@roles_required(3)
def teacher():
    return render_template("teacher.html")
#----------------- ADD COURSE ----------------
@app.route("/add_course", methods=["GET","POST"])
@login_required
@roles_required(3)
def add_course():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO courses (title, description) VALUES (%s,%s)",
            (title, description)
        )
        db.commit()

        cursor.close()
        db.close()

        return redirect("/teacher")
    return render_template("add_course.html")
#----------------- ADD QUESTION ----------------
@app.route("/add_question", methods=["GET","POST"])
@login_required
@roles_required(3)
def add_question():
    if request.method == "POST":
        question = request.form["question"]
        quiz_id = request.form["quiz_id"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO questions (quiz_id, question_text) VALUES (%s,%s)",
            (quiz_id, question)
        )
        db.commit()

        cursor.close()
        db.close()

        return redirect("/teacher")

    return render_template("add_question.html")
#----------------- ADD TOPIC ----------------
@app.route("/add_topic", methods=["GET","POST"])
@login_required
@roles_required(1)
def add_topic():
    if request.method == "POST":
        topic_name = request.form["topic_name"]
        course_id = request.form["course_id"]

        db = get_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO topics (topic_name, course_id) VALUES (%s,%s)",
            (topic_name, course_id)
        )
        db.commit()

        cursor.close()
        db.close()

        return redirect("/admin")

    return render_template("add_topic.html")
#----------------- TEACHER RESULTS ----------------
@app.route("/teacher_results")
@login_required
@roles_required(3)
def teacher_results():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT users.username, quiz_attempts.score, quiz_attempts.total
        FROM quiz_attempts
        JOIN users ON users.user_id = quiz_attempts.user_id
    """)

    data = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("teacher_results.html", data=data)
#----------------- TEACHER REPORT ----------------
@app.route("/teacher_report")
@login_required
@roles_required(3)
def teacher_report():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT users.username, quiz_attempts.score, quiz_attempts.total
        FROM quiz_attempts
        JOIN users ON users.user_id = quiz_attempts.user_id
    """)
    data = cursor.fetchall()

    cursor.close()
    db.close()

    filename = "teacher_report.pdf"
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("Student Performance Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    for d in data:
        text = f"{d['username']} → Score: {d['score']}/{d['total']}"
        elements.append(Paragraph(text, styles["Normal"]))
        elements.append(Spacer(1, 10))

    doc.build(elements)

    from flask import send_file

    return send_file(filename, as_attachment=True)
#----------------- DASHBOARD ----------------

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
#----------------- Delete User----------------
@app.route("/delete_user/<int:user_id>")
@login_required
@roles_required(1)
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM users WHERE user_id=%s", (user_id,))
    db.commit()

    cursor.close()
    db.close()

    return redirect("/admin")
#----------------- COURSE ----------------
@app.route("/course/<int:course_id>")
@login_required
def course_detail(course_id):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # course info
    cursor.execute("SELECT * FROM courses WHERE course_id=%s", (course_id,))
    course = cursor.fetchone()

    # all videos (lessons)
    cursor.execute("""
        SELECT * FROM lessons 
        WHERE course_id=%s 
        ORDER BY position ASC
    """, (course_id,))
    lessons = cursor.fetchall()

    cursor.close()
    db.close()

    return render_template("course_detail.html", course=course, lessons=lessons)
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
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # get user name
    cursor.execute("SELECT username FROM users WHERE user_id=%s", (session["user_id"],))
    user = cursor.fetchone()

    # total lessons
    cursor.execute("SELECT COUNT(*) as total FROM lessons")
    total = cursor.fetchone()["total"]

    # completed lessons
    cursor.execute(
        "SELECT COUNT(*) as completed FROM progress WHERE user_id=%s",
        (session["user_id"],)
    )
    completed = cursor.fetchone()["completed"]

    cursor.close()
    db.close()

    # 🔒 LOCK CHECK
    if completed < total or total == 0:
        return render_template("certificate.html", unlocked=False, completed=completed, total=total)

    # ✅ GENERATE PDF
    filename = f"certificate_{session['user_id']}_{uuid.uuid4().hex[:5]}.pdf"

    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("🎓 Certificate of Completion", styles["Title"]))
    elements.append(Spacer(1, 30))

    elements.append(Paragraph(f"This certifies that", styles["Normal"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph(f"<b>{user['username']}</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("has successfully completed the course", styles["Normal"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("<b>Astronomy Learning Program</b>", styles["Heading2"]))
    elements.append(Spacer(1, 30))

    import datetime
    date = datetime.datetime.now().strftime("%d %B %Y")

    elements.append(Paragraph(f"Date: {date}", styles["Normal"]))

    doc.build(elements)

    return send_file(filename, as_attachment=True)
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
#----------------- PROGRESS ----------------
@app.route("/progress")
@login_required
def progress():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # completed
    cursor.execute(
        "SELECT COUNT(*) as completed FROM progress WHERE user_id=%s",
        (session["user_id"],)
    )
    completed = cursor.fetchone()["completed"]

    # total lessons
    cursor.execute("SELECT COUNT(*) as total FROM lessons")
    total_lessons = cursor.fetchone()["total"]

    cursor.close()
    db.close()

    percentage = int((completed / total_lessons) * 100) if total_lessons > 0 else 0

    return render_template("progress.html", completed=completed, percentage=percentage)

 #----------------- COMPLETE LESSON ----------------
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

    return redirect("/dashboard")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))