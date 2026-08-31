from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import os
from sqlalchemy import text

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "career-bridge-development-key"
)

database_url = os.environ.get("DATABASE_URL")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# =========================================================
# STUDENT DATABASE MODEL
# =========================================================

class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )

    # AI MEMORY
    subjects = db.Column(
        db.Text,
        nullable=True
    )

    skills = db.Column(
        db.Text,
        nullable=True
    )

    interests = db.Column(
        db.Text,
        nullable=True
    )

    career_goal = db.Column(
        db.Text,
        nullable=True
    )


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "student_id" not in session:

            return redirect(
                url_for("login")
            )

        return f(*args, **kwargs)

    return decorated_function


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "home.html"
    )


# =========================================================
# REGISTER
# =========================================================

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = generate_password_hash(
            password
        )

        student = Student(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(student)
        db.session.commit()

        session["student_id"] = student.id
        session["student_name"] = student.name

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        student = Student.query.filter_by(
            email=email
        ).first()

        if not student:

            return "Account not found."

        if not check_password_hash(
            student.password,
            password
        ):

            return "Incorrect password."

        session["student_id"] = student.id
        session["student_name"] = student.name

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# =========================================================
# AI MEMORY - GET
# =========================================================

@app.route(
    "/api/ai-memory",
    methods=["GET"]
)
@login_required
def get_ai_memory():

    student = Student.query.get(
        session["student_id"]
    )

    if not student:

        return jsonify({
            "success": False,
            "message": "Student not found."
        }), 404

    return jsonify({

        "success": True,

        "memory": {

            "subjects": student.subjects or "",

            "skills": student.skills or "",

            "interests": student.interests or "",

            "career_goal": student.career_goal or ""

        }

    })


# =========================================================
# AI MEMORY - SAVE
# =========================================================

@app.route(
    "/api/ai-memory",
    methods=["POST"]
)
@login_required
def save_ai_memory():

    student = Student.query.get(
        session["student_id"]
    )

    if not student:

        return jsonify({
            "success": False,
            "message": "Student not found."
        }), 404

    data = request.get_json(
        silent=True
    ) or {}

    student.subjects = (
        data.get("subjects", "").strip()
    )

    student.skills = (
        data.get("skills", "").strip()
    )

    student.interests = (
        data.get("interests", "").strip()
    )

    student.career_goal = (
        data.get("career_goal", "").strip()
    )

    db.session.commit()

    return jsonify({

        "success": True,

        "message": "AI memory saved successfully.",

        "memory": {

            "subjects": student.subjects or "",

            "skills": student.skills or "",

            "interests": student.interests or "",

            "career_goal": student.career_goal or ""

        }

    })


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    return render_template(
        "dashboard.html"
    )


# =========================================================
# CERTIFICATE
# =========================================================

@app.route("/certificate")
@login_required
def certificate():

    return render_template(
        "certificate.html"
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
@login_required
def about():

    return render_template(
        "about.html"
    )


# =========================================================
# SERVICES
# =========================================================

@app.route("/services")
@login_required
def services():

    return render_template(
        "services.html"
    )


# =========================================================
# COURSES
# =========================================================

@app.route("/courses")
@login_required
def courses():

    return render_template(
        "courses.html"
    )


# =========================================================
# CONTACT
# =========================================================

@app.route("/contact")
@login_required
def contact():

    return render_template(
        "contact.html"
    )


# =========================================================
# PYTHON COURSE
# =========================================================

@app.route("/courses/python")
@login_required
def python():

    return render_template(
        "python.html"
    )


@app.route("/python/module1")
@login_required
def python_module1():

    return render_template(
        "python/module1.html"
    )


@app.route("/python/module2")
@login_required
def python_module2():

    return render_template(
        "python/module2.html"
    )


@app.route("/python/module3")
@login_required
def python_module3():

    return render_template(
        "python/module3.html"
    )


@app.route("/python/module4")
@login_required
def python_module4():

    return render_template(
        "python/module4.html"
    )


@app.route("/python/module5")
@login_required
def python_module5():

    return render_template(
        "python/module5.html"
    )


@app.route("/python/module6")
@login_required
def python_module6():

    return render_template(
        "python/module6.html"
    )


@app.route("/python/module7")
@login_required
def python_module7():

    return render_template(
        "python/module7.html"
    )


@app.route("/python/module8")
@login_required
def python_module8():

    return render_template(
        "python/module8.html"
    )


@app.route("/python/module9")
@login_required
def python_module9():

    return render_template(
        "python/module9.html"
    )


@app.route("/python/module10")
@login_required
def python_module10():

    return render_template(
        "python/module10.html"
    )


# =========================================================
# CV + LINKEDIN COURSE
# =========================================================

@app.route("/courses/cv-linkedin")
@login_required
def cv_linkedin():

    return render_template(
        "cv-linkedin.html"
    )


@app.route("/cv-linkedin/module1")
@login_required
def cv_linkedin_module1():

    return render_template(
        "cv-linkedin/module1.html"
    )


@app.route("/cv-linkedin/module2")
@login_required
def cv_linkedin_module2():

    return render_template(
        "cv-linkedin/module2.html"
    )


@app.route("/cv-linkedin/module3")
@login_required
def cv_linkedin_module3():

    return render_template(
        "cv-linkedin/module3.html"
    )


@app.route("/cv-linkedin/module4")
@login_required
def cv_linkedin_module4():

    return render_template(
        "cv-linkedin/module4.html"
    )


@app.route("/cv-linkedin/module5")
@login_required
def cv_linkedin_module5():

    return render_template(
        "cv-linkedin/module5.html"
    )


# =========================================================
# OTHER COURSES
# =========================================================

@app.route("/courses/digital-skills")
@login_required
def digital_skills():

    return render_template(
        "digital-skills.html"
    )


@app.route("/courses/career-development")
@login_required
def career_development():

    return render_template(
        "career-development.html"
    )


# =========================================================
# AI ASSISTANT PAGE
# =========================================================

@app.route("/ai-assistant")
@login_required
def ai_assistant():

    return render_template(
        "ai-assistant.html"
    )


# =========================================================
# LIBRARY
# =========================================================

@app.route("/library")
@login_required
def library():

    return render_template(
        "library.html"
    )


# =========================================================
# OPPORTUNITIES
# =========================================================

@app.route("/opportunities")
@login_required
def opportunities():

    opportunities = [

        {
            "title": "Nigerian Scholarship Award",
            "organization": "Federal Scholarship Board",
            "category": "Scholarships",
            "description":
                "Federal scholarship support for eligible Nigerian students.",
            "deadline":
                "Check official portal",
            "location":
                "Nigeria",
            "link":
                "https://scholarship.education.gov.ng/"
        },

        {
            "title": "Student Venture Capital Grant",
            "organization":
                "Federal Ministry of Education",
            "category":
                "Career Programmes",
            "description":
                "Support for eligible student-led businesses and innovative projects.",
            "deadline":
                "Check official portal",
            "location":
                "Nigeria",
            "link":
                "https://svcg.education.gov.ng/"
        },

        {
            "title":
                "Presidential Amnesty Programme Scholarship",
            "organization":
                "Presidential Amnesty Programme",
            "category":
                "Scholarships",
            "description":
                "Scholarship support for eligible students from the Niger Delta.",
            "deadline":
                "Applications closed",
            "location":
                "Niger Delta, Nigeria",
            "link":
                "https://osapnd.gov.ng/scholarship/"
        },

        {
            "title": "3MTT",
            "organization":
                "Federal Government of Nigeria",
            "category":
                "Free Courses",
            "description":
                "A national programme for developing practical digital and technology skills.",
            "deadline":
                "Check official portal",
            "location":
                "Nigeria",
            "link":
                "https://3mtt.nitda.gov.ng/"
        }

    ]

    return render_template(
        "opportunities.html",
        opportunities=opportunities
    )


# =========================================================
# CAREER EXPLORER
# =========================================================

@app.route("/career-explorer")
@login_required
def career_explorer():

    return render_template(
        "career-explorer.html"
    )


# =========================================================
# BLOG
# =========================================================

@app.route("/blog")
@login_required
def blog():

    return render_template(
        "blog.html"
    )


# =========================================================
# CAREER QUIZ
# =========================================================

@app.route("/career-quiz")
@login_required
def career_quiz():

    return render_template(
        "career-quiz.html"
    )


# =========================================================
# CV BUILDER
# =========================================================

@app.route("/cv-builder")
@login_required
def cv_builder():

    return render_template(
        "cv-builder.html"
    )


# =========================================================
# PYTHON PLAYGROUND
# =========================================================

@app.route("/python/playground")
@login_required
def python_playground():

    return render_template(
        "python/playground.html"
    )


# =========================================================
# DATABASE SETUP + SAFE MIGRATION
# =========================================================

with app.app_context():

    db.create_all()

    try:

        memory_columns = {
            "subjects": "TEXT",
            "skills": "TEXT",
            "interests": "TEXT",
            "career_goal": "TEXT"
        }

        for column_name, column_type in memory_columns.items():

            db.session.execute(
                text(
                    f"""
                    ALTER TABLE student
                    ADD COLUMN IF NOT EXISTS {column_name} {column_type}
                    """
                )
            )

        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            "Database migration warning:",
            e
        )

# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
