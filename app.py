from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"

# DATABASE CONNECTION
db = mysql.connector.connect(
    host="localhost",
    user="astro_user",
    password="1234",
    database="astronomy_db"
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
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validation
        if not username or not email or not password:
            return render_template("register.html", error="All fields are required")

        try:
            # Check duplicate
            cursor.execute(
                "SELECT * FROM users WHERE username=%s OR email=%s",
                (username, email)
            )
            if cursor.fetchone():
                return render_template("register.html", error="User already exists")

            # Insert user
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                (username, email, password)
            )
            db.commit()

        except Exception as e:
            print(e)
            return render_template("register.html", error="Database error")

        return render_template("login.html", success="Account created successfully")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("login.html", error="All fields are required")

        try:
            cursor.execute("SELECT * FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()
        except Exception as e:
            print(e)
            return render_template("login.html", error="Database error")

        if not user:
            return render_template("login.html", error="User not found")

        if user["password"] != password:
            return render_template("login.html", error="Wrong password")

        session["user"] = user["username"]
        return redirect(url_for("quiz"))

    return render_template("login.html")


# ---------------- QUIZ ----------------
@app.route("/quiz", methods=["GET", "POST"])
def quiz():
    if not session.get("user"):
        return redirect(url_for("login"))

    try:
        cursor.execute("SELECT * FROM questions")
        questions = cursor.fetchall()
    except Exception as e:
        print(e)
        return "Database error"

    if not questions:
        return "No questions available"

    if request.method == "POST":
        score = 0

        for q in questions:
            selected = request.form.get(f"q{q['question_id']}")

            if selected is None:
                continue

            if selected == q["correct_answer"]:
                score += 1

        # SAVE SCORE
        username = session.get("user")

        try:
            cursor.execute(
                "INSERT INTO scores (username, score, total) VALUES (%s, %s, %s)",
                (username, score, len(questions))
            )
            db.commit()
        except Exception as e:
            print(e)
            return "Database error while saving score"

        return render_template("result.html", score=score, total=len(questions))

    return render_template("quiz.html", questions=questions)


# ---------------- PROGRESS ----------------
@app.route("/progress")
def progress():
    if not session.get("user"):
        return redirect(url_for("login"))

    username = session.get("user")

    try:
        cursor.execute("SELECT * FROM scores WHERE username=%s", (username,))
        scores = cursor.fetchall()
    except Exception as e:
        print(e)
        return "Database error"

    if not scores:
        return render_template("progress.html", message="No attempts yet")

    total_attempts = len(scores)

    best_score = 0
    total_score = 0

    for s in scores:
        total_score += s["score"]
        if s["score"] > best_score:
            best_score = s["score"]

    average_score = total_score / total_attempts if total_attempts > 0 else 0

    return render_template(
        "progress.html",
        scores=scores,
        total_attempts=total_attempts,
        best_score=best_score,
        average_score=round(average_score, 2)
    )


# ---------------- CONTENT PAGES ----------------
@app.route("/planets")
def planets():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("planets.html")


@app.route("/stars")
def stars():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("stars.html")


@app.route("/galaxies")
def galaxies():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("galaxies.html")


@app.route("/blackholes")
def blackholes():
    if not session.get("user"):
        return redirect(url_for("login"))
    return render_template("blackholes.html")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)