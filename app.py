from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "career-bridge-development-key"
)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///career_bridge.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

from functools import wraps

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "student_id" not in session:
            return redirect(url_for("login"))

        return f(*args, **kwargs)

    return decorated_function


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_password = generate_password_hash(password)

        student = Student(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(student)
        db.session.commit()

        session["student_id"] = student.id

        return redirect("/dashboard")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        student = Student.query.filter_by(email=email).first()

        if not student:
            return "Account not found."

        if not check_password_hash(student.password, password):
            return "Incorrect password."

        session["student_id"] = student.id
        session["student_name"] = student.name

        return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")


@app.route("/certificate")
@login_required
def certificate():
    return render_template("certificate.html")


@app.route("/about")
@login_required
def certificate():
    return render_template("about.html")


@app.route("/services")
@login_required
def services():
    return render_template("services.html")


@app.route("/courses")
@login_required
def courses():
    return render_template("courses.html")


@app.route("/contact")
@login_required
def contact():
    return render_template("contact.html")


@app.route("/courses/python")
@login_required
def python():
    return render_template("python.html")


@app.route("/python/module1")
@login_required
def python_module1():
    return render_template("python/module1.html")

@app.route("/python/module2")
@login_required
def python_module2():
    return render_template("python/module2.html")

@app.route("/python/module3")
@login_required
def python_module3():
    return render_template("python/module3.html")


@app.route("/python/module4")
@login_required
def python_module4():
    return render_template("python/module4.html")


@app.route("/python/module5")
@login_required
def python_module5():
    return render_template("python/module5.html")


@app.route("/python/module6")
@login_required
def python_module6():
    return render_template("python/module6.html")


@app.route("/python/module7")
@login_required
def python_module7():
    return render_template("python/module7.html")


@app.route("/python/module8")
@login_required
def python_module8():
    return render_template("python/module8.html")


@app.route("/python/module9")
@login_required
def python_module9():
    return render_template("python/module9.html")


@app.route("/python/module10")
@login_required
def python_module10():
    return render_template("python/module10.html")


@app.route("/courses/cv-linkedin")
@login_required
def cv_linkedin():
    return render_template("cv-linkedin.html")


@app.route("/cv-linkedin/module1")
@login_required
def cv_linkedin_module1():
    return render_template("cv-linkedin/module1.html")

@app.route("/cv-linkedin/module2")
@login_required
def cv_linkedin_module2():
    return render_template("cv-linkedin/module2.html")

@app.route("/cv-linkedin/module3")
@login_required
def cv_linkedin_module3():
    return render_template("cv-linkedin/module3.html")

@app.route("/cv-linkedin/module4")
@login_required
def cv_linkedin_module4():
    return render_template("cv-linkedin/module4.html")

@app.route("/cv-linkedin/module5")
@login_required
def cv_linkedin_module5():
    return render_template("cv-linkedin/module5.html")


@app.route("/courses/digital-skills")
@login_required
def digital_skills():
    return render_template("digital-skills.html")


@app.route("/courses/career-development")
@login_required
def career_development():
    return render_template("career-development.html")


@app.route("/library")
@login_required
def library():
    return render_template("library.html")


@app.route("/opportunities")
@login_required
def opportunities():

    opportunities = [
        {
            "title": "Nigerian Scholarship Award",
            "organization": "Federal Scholarship Board",
            "category": "Scholarships",
            "description": "Federal scholarship support for eligible Nigerian students.",
            "deadline": "Check official portal",
            "location": "Nigeria",
            "link": "https://scholarship.education.gov.ng/"
        },

        {
            "title": "Student Venture Capital Grant",
            "organization": "Federal Ministry of Education",
            "category": "Career Programmes",
            "description": "Support for eligible student-led businesses and innovative projects.",
            "deadline": "Check official portal",
            "location": "Nigeria",
            "link": "https://svcg.education.gov.ng/"
        },

        {
            "title": "Presidential Amnesty Programme Scholarship",
            "organization": "Presidential Amnesty Programme",
            "category": "Scholarships",
            "description": "Scholarship support for eligible students from the Niger Delta.",
            "deadline": "Applications closed",
            "location": "Niger Delta, Nigeria",
            "link": "https://osapnd.gov.ng/scholarship/"
        },

        {
            "title": "3MTT",
            "organization": "Federal Government of Nigeria",
            "category": "Free Courses",
            "description": "A national programme for developing practical digital and technology skills.",
            "deadline": "Check official portal",
            "location": "Nigeria",
            "link": "https://3mtt.nitda.gov.ng/"
        }
    ]

    return render_template("opportunities.html", opportunities=opportunities)
            
            
@app.route("/career-explorer")
@login_required
def career_explorer():
    return render_template("career-explorer.html")


@app.route("/blog")
@login_required
def blog():
    return render_template("blog.html")


@app.route("/career-quiz")
@login_required
def career_quiz():
    return render_template("career-quiz.html")


@app.route("/cv-builder")
@login_required
def cv_builder():
    return render_template("cv-builder.html")

@app.route("/python/playground")
@login_required
def python_playground():
    return render_template("python/playground.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
