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


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if not name or not email or not password:
            return "Please fill in all fields."

        existing_student = Student.query.filter_by(
            email=email
        ).first()

        if existing_student:
            return "An account with this email already exists."

        hashed_password = generate_password_hash(password)

        student = Student(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(student)
        db.session.commit()

        session["student_id"] = student.id
        session["student_name"] = student.name

        return redirect(url_for("dashboard"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get("email")
        password = request.form.get("password")

        student = Student.query.filter_by(
            email=email
        ).first()

        if student and check_password_hash(
            student.password,
            password
        ):

            session["student_id"] = student.id
            session["student_name"] = student.name

            return redirect(url_for("dashboard"))

        return "Invalid email or password."

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/certificate")
def certificate():
    return render_template("certificate.html")


@app.route("/services")
def services():
    return render_template("services.html")


@app.route("/courses")
def courses():
    return render_template("courses.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/courses/python")
def python():
    return render_template("python.html")


@app.route("/python/module1")
def python_module1():
    return render_template("python/module1.html")


@app.route("/python/module2")
def python_module2():
    return render_template("python/module2.html")


@app.route("/python/module3")
def python_module3():
    return render_template("python/module3.html")


@app.route("/python/module4")
def python_module4():
    return render_template("python/module4.html")


@app.route("/python/module5")
def python_module5():
    return render_template("python/module5.html")


@app.route("/python/module6")
def python_module6():
    return render_template("python/module6.html")


@app.route("/python/module7")
def python_module7():
    return render_template("python/module7.html")


@app.route("/python/module8")
def python_module8():
    return render_template("python/module8.html")


@app.route("/python/module9")
def python_module9():
    return render_template("python/module9.html")


@app.route("/python/module10")
def python_module10():
    return render_template("python/module10.html")


@app.route("/courses/cv-linkedin")
def cv_linkedin():
    return render_template("cv-linkedin.html")


@app.route("/cv-linkedin/module1")
def cv_linkedin_module1():
    return render_template("cv-linkedin/module1.html")

@app.route("/cv-linkedin/module2")
def cv_linkedin_module2():
    return render_template("cv-linkedin/module2.html")

@app.route("/cv-linkedin/module3")
def cv_linkedin_module3():
    return render_template("cv-linkedin/module3.html")

@app.route("/cv-linkedin/module4")
def cv_linkedin_module4():
    return render_template("cv-linkedin/module4.html")

@app.route("/cv-linkedin/module5")
def cv_linkedin_module5():
    return render_template("cv-linkedin/module5.html")


@app.route("/courses/digital-skills")
def digital_skills():
    return render_template("digital-skills.html")


@app.route("/courses/career-development")
def career_development():
    return render_template("career-development.html")


@app.route("/library")
def library():
    return render_template("library.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/opportunities")
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
def career_explorer():
    return render_template("career-explorer.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/career-quiz")
def career_quiz():
    return render_template("career-quiz.html")


@app.route("/cv-builder")
def cv_builder():
    return render_template("cv-builder.html")

@app.route("/python/playground")
def python_playground():
    return render_template("python/playground.html")


with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)
