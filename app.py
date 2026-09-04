from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
from sqlalchemy import inspect, text
import os
import json
import random


# =========================================================
# APP SETUP
# =========================================================

app = Flask(__name__)


# =========================================================
# JSON TEMPLATE FILTER
# =========================================================

@app.template_filter("from_json")
def from_json_filter(value):

    try:
        return json.loads(value)

    except (TypeError, ValueError, json.JSONDecodeError):
        return []


# =========================================================
# SECRET KEY
# =========================================================

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "career-bridge-development-key"
)


# =========================================================
# DATABASE
# =========================================================

database_url = os.environ.get("DATABASE_URL")

if not database_url:

    database_url = "sqlite:///career_bridge.db"


if database_url.startswith("postgres://"):

    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1
    )


app.config["SQLALCHEMY_DATABASE_URI"] = database_url

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


db = SQLAlchemy(app)


# =========================================================
# STUDENT MODEL
# =========================================================

class Student(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

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
# MENTOR MODEL
# =========================================================

class Mentor(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    profession = db.Column(
        db.String(150),
        nullable=False
    )

    field = db.Column(
        db.String(100),
        nullable=False
    )

    bio = db.Column(
        db.Text,
        nullable=True
    )

    skills = db.Column(
        db.Text,
        nullable=True
    )

    experience = db.Column(
        db.Text,
        nullable=True
    )

    email = db.Column(
        db.String(120),
        nullable=True
    )

    verified = db.Column(
        db.Boolean,
        default=False
    )


# =========================================================
# ADMIN MODEL
# =========================================================

class Admin(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(200),
        nullable=False
    )


# =========================================================
# MENTORSHIP REQUEST MODEL
# =========================================================

class MentorshipRequest(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    mentor_id = db.Column(
        db.Integer,
        db.ForeignKey("mentor.id"),
        nullable=False
    )

    message = db.Column(
        db.Text,
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending",
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "mentorship_requests",
            lazy=True
        )
    )

    mentor = db.relationship(
        "Mentor",
        backref=db.backref(
            "mentorship_requests",
            lazy=True
        )
    )


# =========================================================
# DIGITAL SKILLS PROGRESS MODEL
# =========================================================

class DigitalSkillsProgress(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    module_number = db.Column(
        db.Integer,
        nullable=False
    )

    completed = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    quiz_score = db.Column(
        db.Integer,
        nullable=True
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "digital_skills_progress",
            lazy=True
        )
    )

    __table_args__ = (
        db.UniqueConstraint(
            "student_id",
            "module_number",
            name="unique_student_digital_module"
        ),
    )


# =========================================================
# JAMB QUESTION MODEL
# =========================================================

class JAMBQuestion(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    year = db.Column(
        db.Integer,
        nullable=True,
        index=True
    )

    subject = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    topic = db.Column(
        db.String(150),
        nullable=True,
        index=True
    )

    subtopic = db.Column(
        db.String(150),
        nullable=True,
        index=True
    )

    difficulty = db.Column(
        db.String(30),
        nullable=True
    )

    question = db.Column(
        db.Text,
        nullable=False
    )

    option_a = db.Column(
        db.Text,
        nullable=False
    )

    option_b = db.Column(
        db.Text,
        nullable=False
    )

    option_c = db.Column(
        db.Text,
        nullable=False
    )

    option_d = db.Column(
        db.Text,
        nullable=False
    )

    correct_answer = db.Column(
        db.String(1),
        nullable=False
    )

    explanation = db.Column(
        db.Text,
        nullable=True
    )

    source = db.Column(
        db.String(200),
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================================================
# JAMB EXAM ATTEMPT MODEL
# =========================================================

class JAMBExamAttempt(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("student.id"),
        nullable=False
    )

    subjects = db.Column(
        db.Text,
        nullable=False
    )

    year = db.Column(
        db.Integer,
        nullable=True
    )

    total_questions = db.Column(
        db.Integer,
        nullable=False
    )

    correct_answers = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    score = db.Column(
        db.Integer,
        default=0,
        nullable=False
    )

    started_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    student = db.relationship(
        "Student",
        backref=db.backref(
            "jamb_attempts",
            lazy=True
        )
    )


# =========================================================
# STUDENT LOGIN REQUIRED
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
# ADMIN LOGIN REQUIRED
# =========================================================

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if "admin_id" not in session:

            return redirect(
                url_for("admin_login")
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

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        if not name or not email or not password:

            return (
                "Please fill in all fields.",
                400
            )


        existing_student = Student.query.filter_by(
            email=email
        ).first()


        if existing_student:

            return (
                "An account with this email already exists.",
                400
            )


        student = Student(
            name=name,
            email=email,
            password=generate_password_hash(
                password
            )
        )


        db.session.add(
            student
        )

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

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        student = Student.query.filter_by(
            email=email
        ).first()


        if not student:

            return (
                "Account not found.",
                404
            )


        if not check_password_hash(
            student.password,
            password
        ):

            return (
                "Incorrect password.",
                401
            )


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

    session.pop(
        "student_id",
        None
    )

    session.pop(
        "student_name",
        None
    )

    session.pop(
        "jamb_year",
        None
    )

    session.pop(
        "jamb_subjects",
        None
    )

    session.pop(
        "jamb_question_count",
        None
    )

    session.pop(
        "jamb_question_ids",
        None
    )

    session.pop(
        "jamb_started_at",
        None
    )

    session.pop(
        "jamb_last_attempt_id",
        None
    )


    return redirect(
        url_for("login")
    )


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route(
    "/admin/login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )


        admin = Admin.query.filter_by(
            username=username
        ).first()


        if not admin:

            return (
                "Admin account not found.",
                404
            )


        if not check_password_hash(
            admin.password,
            password
        ):

            return (
                "Incorrect admin password.",
                401
            )


        session["admin_id"] = admin.id

        session["admin_username"] = admin.username


        return redirect(
            url_for("admin_dashboard")
        )


    return render_template(
        "admin-login.html"
    )


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/admin/logout")
def admin_logout():

    session.pop(
        "admin_id",
        None
    )

    session.pop(
        "admin_username",
        None
    )


    return redirect(
        url_for("admin_login")
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():

    mentors = Mentor.query.order_by(
        Mentor.name.asc()
    ).all()


    mentorship_requests = MentorshipRequest.query.order_by(
        MentorshipRequest.id.desc()
    ).all()


    students = Student.query.order_by(
        Student.id.desc()
    ).all()


    return render_template(
        "admin-dashboard.html",
        mentors=mentors,
        mentorship_requests=mentorship_requests,
        students=students
    )


# =========================================================
# ADD MENTOR
# =========================================================

@app.route(
    "/add-mentor",
    methods=["GET", "POST"]
)
@admin_required
def add_mentor():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        profession = request.form.get(
            "profession",
            ""
        ).strip()

        field = request.form.get(
            "field",
            ""
        ).strip()

        bio = request.form.get(
            "bio",
            ""
        ).strip()

        skills = request.form.get(
            "skills",
            ""
        ).strip()

        experience = request.form.get(
            "experience",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()


        if not name or not profession or not field:

            return (
                "Name, profession and field are required.",
                400
            )


        mentor = Mentor(
            name=name,
            profession=profession,
            field=field,
            bio=bio,
            skills=skills,
            experience=experience,
            email=email,
            verified=True
        )


        db.session.add(
            mentor
        )

        db.session.commit()


        return redirect(
            url_for("admin_dashboard")
        )


    return render_template(
        "add-mentor.html"
    )


# =========================================================
# DELETE MENTOR
# =========================================================

@app.route(
    "/admin/delete-mentor/<int:mentor_id>",
    methods=["POST"]
)
@admin_required
def delete_mentor(mentor_id):

    mentor = Mentor.query.get_or_404(
        mentor_id
    )


    MentorshipRequest.query.filter_by(
        mentor_id=mentor.id
    ).delete(
        synchronize_session=False
    )


    db.session.delete(
        mentor
    )

    db.session.commit()


    return redirect(
        url_for("admin_dashboard")
    )


# =========================================================
# MENTORS
# =========================================================

@app.route("/mentors")
@login_required
def mentors():

    mentors_list = Mentor.query.filter_by(
        verified=True
    ).order_by(
        Mentor.name.asc()
    ).all()


    return render_template(
        "mentors.html",
        mentors=mentors_list
    )


# =========================================================
# MENTOR PROFILE
# =========================================================

@app.route(
    "/mentor/<int:mentor_id>"
)
@login_required
def mentor_profile(mentor_id):

    mentor = Mentor.query.get_or_404(
        mentor_id
    )


    if not mentor.verified:

        return (
            "Mentor not available.",
            404
        )


    return render_template(
        "mentor-profile.html",
        mentor=mentor
    )


# =========================================================
# REQUEST MENTORSHIP
# =========================================================

@app.route(
    "/mentor/<int:mentor_id>/request",
    methods=["GET", "POST"]
)
@login_required
def request_mentorship(mentor_id):

    mentor = Mentor.query.get_or_404(
        mentor_id
    )


    if not mentor.verified:

        return (
            "Mentor not available.",
            404
        )


    if request.method == "POST":

        message = request.form.get(
            "message",
            ""
        ).strip()


        if not message:

            return (
                "Please enter a message.",
                400
            )


        mentorship_request = MentorshipRequest(
            student_id=session["student_id"],
            mentor_id=mentor.id,
            message=message,
            status="Pending"
        )


        db.session.add(
            mentorship_request
        )

        db.session.commit()


        return redirect(
            url_for(
                "my_mentorship_requests"
            )
        )


    return render_template(
        "request-mentorship.html",
        mentor=mentor
    )


# =========================================================
# MY MENTORSHIP REQUESTS
# =========================================================

@app.route(
    "/my-mentorship-requests"
)
@login_required
def my_mentorship_requests():

    requests = MentorshipRequest.query.filter_by(
        student_id=session["student_id"]
    ).order_by(
        MentorshipRequest.id.desc()
    ).all()


    return render_template(
        "my-mentorship-requests.html",
        requests=requests
    )


# =========================================================
# ADMIN MENTORSHIP REQUESTS
# =========================================================

@app.route(
    "/admin/mentorship-requests"
)
@admin_required
def admin_mentorship_requests():

    requests = MentorshipRequest.query.order_by(
        MentorshipRequest.id.desc()
    ).all()


    return render_template(
        "admin-mentorship-requests.html",
        requests=requests
    )


# =========================================================
# UPDATE MENTORSHIP REQUEST
# =========================================================

@app.route(
    "/admin/mentorship-request/<int:request_id>/<status>",
    methods=["GET", "POST"]
)
@admin_required
def update_mentorship_request(
    request_id,
    status
):

    allowed_statuses = [
        "Pending",
        "Accepted",
        "Declined"
    ]


    if status not in allowed_statuses:

        return (
            "Invalid status.",
            400
        )


    mentorship_request = MentorshipRequest.query.get_or_404(
        request_id
    )


    mentorship_request.status = status

    db.session.commit()


    return redirect(
        url_for(
            "admin_mentorship_requests"
        )
    )


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
@login_required
def dashboard():

    student_id = session["student_id"]


    completed_modules = DigitalSkillsProgress.query.filter_by(
        student_id=student_id,
        completed=True
    ).count()


    progress_percent = int(
        (completed_modules / 10) * 100
    )


    mentorship_requests = MentorshipRequest.query.filter_by(
        student_id=student_id
    ).order_by(
        MentorshipRequest.id.desc()
    ).all()


    return render_template(
        "dashboard.html",
        completed_modules=completed_modules,
        progress_percent=progress_percent,
        mentorship_requests=mentorship_requests
    )


# =========================================================
# CERTIFICATE
# =========================================================

@app.route("/certificate")
@login_required
def certificate():

    completed_modules = DigitalSkillsProgress.query.filter_by(
        student_id=session["student_id"],
        completed=True
    ).count()


    return render_template(
        "certificate.html",
        completed_modules=completed_modules,
        digital_skills_complete=(
            completed_modules >= 10
        )
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


# =========================================================
# PYTHON MODULES
# =========================================================

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
# DIGITAL SKILLS COURSE
# =========================================================

@app.route("/courses/digital-skills")
@login_required
def digital_skills():

    student_id = session["student_id"]


    completed_modules = DigitalSkillsProgress.query.filter_by(
        student_id=student_id,
        completed=True
    ).count()


    progress_percent = int(
        (completed_modules / 10) * 100
    )


    return render_template(
        "digital-skills.html",
        completed_modules=completed_modules,
        progress_percent=progress_percent
    )


# =========================================================
# DIGITAL SKILLS MODULES
# =========================================================

@app.route("/digital-skills/module1")
@login_required
def digital_skills_module1():

    return render_template(
        "digital-skills/module1.html",
        module_number=1
    )


@app.route("/digital-skills/module2")
@login_required
def digital_skills_module2():

    return render_template(
        "digital-skills/module2.html",
        module_number=2
    )


@app.route("/digital-skills/module3")
@login_required
def digital_skills_module3():

    return render_template(
        "digital-skills/module3.html",
        module_number=3
    )


@app.route("/digital-skills/module4")
@login_required
def digital_skills_module4():

    return render_template(
        "digital-skills/module4.html",
        module_number=4
    )


@app.route("/digital-skills/module5")
@login_required
def digital_skills_module5():

    return render_template(
        "digital-skills/module5.html",
        module_number=5
    )


@app.route("/digital-skills/module6")
@login_required
def digital_skills_module6():

    return render_template(
        "digital-skills/module6.html",
        module_number=6
    )


@app.route("/digital-skills/module7")
@login_required
def digital_skills_module7():

    return render_template(
        "digital-skills/module7.html",
        module_number=7
    )


@app.route("/digital-skills/module8")
@login_required
def digital_skills_module8():

    return render_template(
        "digital-skills/module8.html",
        module_number=8
    )


@app.route("/digital-skills/module9")
@login_required
def digital_skills_module9():

    return render_template(
        "digital-skills/module9.html",
        module_number=9
    )


@app.route("/digital-skills/module10")
@login_required
def digital_skills_module10():

    return render_template(
        "digital-skills/module10.html",
        module_number=10
    )


# =========================================================
# DIGITAL SKILLS PROGRESS
# =========================================================

@app.route("/digital-skills/progress")
@login_required
def digital_skills_progress():

    student_id = session["student_id"]


    progress_records = DigitalSkillsProgress.query.filter_by(
        student_id=student_id
    ).order_by(
        DigitalSkillsProgress.module_number.asc()
    ).all()


    completed_numbers = {
        record.module_number
        for record in progress_records
        if record.completed
    }


    completed_modules = len(
        completed_numbers
    )


    progress_percent = int(
        (completed_modules / 10) * 100
    )


    return render_template(
        "digital-skills-progress.html",
        progress=progress_records,
        completed_modules=completed_modules,
        progress_percent=progress_percent,
        completed_numbers=completed_numbers
    )


# =========================================================
# COMPLETE DIGITAL SKILLS MODULE
# =========================================================

@app.route(
    "/digital-skills/module/<int:module_number>/complete",
    methods=["POST"]
)
@login_required
def complete_digital_skills_module(
    module_number
):

    if module_number < 1 or module_number > 10:

        return (
            "Invalid module.",
            400
        )


    record = DigitalSkillsProgress.query.filter_by(
        student_id=session["student_id"],
        module_number=module_number
    ).first()


    if not record:

        record = DigitalSkillsProgress(
            student_id=session["student_id"],
            module_number=module_number,
            completed=False
        )

        db.session.add(
            record
        )


    record.completed = True

    record.completed_at = datetime.utcnow()


    quiz_score = request.form.get(
        "quiz_score"
    )


    if quiz_score is not None and quiz_score != "":

        try:

            record.quiz_score = int(
                quiz_score
            )

        except ValueError:

            pass


    db.session.commit()


    return redirect(
        url_for(
            "digital_skills_progress"
        )
    )


# =========================================================
# DIGITAL SKILLS API
# =========================================================

@app.route(
    "/api/digital-skills-progress",
    methods=["GET"]
)
@login_required
def digital_skills_progress_api():

    records = DigitalSkillsProgress.query.filter_by(
        student_id=session["student_id"],
        completed=True
    ).order_by(
        DigitalSkillsProgress.module_number.asc()
    ).all()


    completed_modules = [
        record.module_number
        for record in records
    ]


    total = 10

    completed = len(
        completed_modules
    )


    percentage = int(
        (completed / total) * 100
    )


    return jsonify({
        "success": True,
        "completed_modules": completed_modules,
        "completed": completed,
        "total": total,
        "percentage": percentage
    })


# =========================================================
# EXAM PREPARATION
# =========================================================

@app.route("/exam-preparation")
@login_required
def exam_preparation():

    subjects = [
        "Use of English",
        "Mathematics",
        "Physics",
        "Chemistry",
        "Biology",
        "Economics",
        "Government",
        "Literature",
        "Geography",
        "Commerce",
        "Accounting",
        "Agricultural Science",
        "Computer Science"
    ]


    return render_template(
        "exam-preparation.html",
        subjects=subjects
    )


# =========================================================
# START JAMB EXAM
# =========================================================

@app.route(
    "/exam-preparation/jamb/start",
    methods=["POST"]
)
@login_required
def start_jamb_exam():

    selected_subjects = request.form.getlist(
        "subjects"
    )


    selected_question_count = request.form.get(
        "question_count",
        ""
    ).strip()


    # -----------------------------------------------------
    # QUESTION COUNT
    # -----------------------------------------------------

    if not selected_question_count:

        return (
            "Please select the number of questions.",
            400
        )


    try:

        selected_question_count = int(
            selected_question_count
        )

    except (ValueError, TypeError):

        return (
            "Invalid question count.",
            400
        )


    allowed_question_counts = [
        20,
        40,
        60,
        100
    ]


    if selected_question_count not in allowed_question_counts:

        return (
            "Invalid question count.",
            400
        )


    # -----------------------------------------------------
    # SUBJECTS
    # -----------------------------------------------------

    if not selected_subjects:

        return (
            "Please select at least one subject.",
            400
        )


    cleaned_subjects = []


    for subject in selected_subjects:

        subject = subject.strip()


        if subject and subject not in cleaned_subjects:

            cleaned_subjects.append(
                subject
            )


    if not cleaned_subjects:

        return (
            "Please select at least one subject.",
            400
        )


    # -----------------------------------------------------
    # ALLOWED SUBJECTS
    # -----------------------------------------------------

    allowed_subjects = [
        "Use of English",
        "Mathematics",
        "Physics",
        "Chemistry",
        "Biology",
        "Economics",
        "Government",
        "Literature",
        "Geography",
        "Commerce",
        "Accounting",
        "Agricultural Science",
        "Computer Science"
    ]


    invalid_subjects = [
        subject
        for subject in cleaned_subjects
        if subject not in allowed_subjects
    ]


    if invalid_subjects:

        return (
            "One or more selected subjects are invalid.",
            400
        )


    # -----------------------------------------------------
    # SAVE EXAM SETTINGS
    # -----------------------------------------------------

    session.pop(
        "jamb_year",
        None
    )


    session["jamb_subjects"] = cleaned_subjects


    session["jamb_question_count"] = (
        selected_question_count
    )


    session.pop(
        "jamb_question_ids",
        None
    )


    session.pop(
        "jamb_started_at",
        None
    )


    return redirect(
        url_for("jamb_exam")
    )


# =========================================================
# JAMB EXAM
# =========================================================

@app.route(
    "/exam-preparation/jamb/exam"
)
@login_required
def jamb_exam():

    selected_subjects = session.get(
        "jamb_subjects",
        []
    )


    selected_question_count = session.get(
        "jamb_question_count"
    )


    if (
        not selected_subjects
        or not selected_question_count
    ):

        return redirect(
            url_for("exam_preparation")
        )


    try:

        selected_question_count = int(
            selected_question_count
        )

    except (ValueError, TypeError):

        return redirect(
            url_for("exam_preparation")
        )


    # -----------------------------------------------------
    # GET QUESTIONS
    # -----------------------------------------------------

    all_available_questions = []

    questions_by_subject = {}


    for subject in selected_subjects:

        subject_questions = JAMBQuestion.query.filter(
            JAMBQuestion.subject == subject
        ).all()


        random.shuffle(
            subject_questions
        )


        questions_by_subject[subject] = (
            subject_questions
        )


        all_available_questions.extend(
            subject_questions
        )


    # -----------------------------------------------------
    # TOTAL AVAILABLE
    # -----------------------------------------------------

    total_available = len(
        all_available_questions
    )


    if total_available == 0:

        return (
            """
            <h2>No questions are currently available.</h2>

            <p>
                The Career Bridge question bank has not been
                populated yet.
            </p>

            <p>
                Please make sure
                <strong>seed_jamb.py</strong>
                is present in your project and redeploy the app.
            </p>
            """,
            404
        )


    # -----------------------------------------------------
    # NOT ENOUGH QUESTIONS
    # -----------------------------------------------------

    if total_available < selected_question_count:

        return (
            f"""
            <h2>Not enough questions available.</h2>

            <p>
                You requested
                <strong>{selected_question_count}</strong>
                questions.
            </p>

            <p>
                Only
                <strong>{total_available}</strong>
                questions are currently available.
            </p>

            <p>
                Please choose a smaller question count or
                select another subject.
            </p>
            """,
            400
        )


    # -----------------------------------------------------
    # FAIR DISTRIBUTION
    # -----------------------------------------------------

    subject_count = len(
        selected_subjects
    )


    base_questions_per_subject = (
        selected_question_count
        //
        subject_count
    )


    remainder = (
        selected_question_count
        %
        subject_count
    )


    final_questions = []

    remaining_question_pool = {}


    # -----------------------------------------------------
    # FIRST PASS
    # -----------------------------------------------------

    for index, subject in enumerate(
        selected_subjects
    ):

        available_questions = questions_by_subject.get(
            subject,
            []
        )


        target_count = (
            base_questions_per_subject
        )


        if index < remainder:

            target_count += 1


        selected_for_subject = (
            available_questions[:target_count]
        )


        final_questions.extend(
            selected_for_subject
        )


        remaining_question_pool[subject] = (
            available_questions[target_count:]
        )


    # -----------------------------------------------------
    # SECOND PASS
    # -----------------------------------------------------

    if len(final_questions) < selected_question_count:

        remaining_needed = (
            selected_question_count
            -
            len(final_questions)
        )


        extra_pool = []


        for subject in selected_subjects:

            extra_pool.extend(
                remaining_question_pool.get(
                    subject,
                    []
                )
            )


        random.shuffle(
            extra_pool
        )


        final_questions.extend(
            extra_pool[:remaining_needed]
        )


    # -----------------------------------------------------
    # FINAL CHECK
    # -----------------------------------------------------

    if len(final_questions) < selected_question_count:

        return (
            "There are not enough questions available "
            "to create this practice session.",
            400
        )


    # -----------------------------------------------------
    # RANDOMIZE QUESTION ORDER
    # -----------------------------------------------------

    random.shuffle(
        final_questions
    )


    final_questions = final_questions[
        :selected_question_count
    ]


    # -----------------------------------------------------
    # SAVE QUESTION IDS
    # -----------------------------------------------------

    session["jamb_question_ids"] = [
        question.id
        for question in final_questions
    ]


    # -----------------------------------------------------
    # START TIME
    # -----------------------------------------------------

    session["jamb_started_at"] = (
        datetime.utcnow().isoformat()
    )


    # -----------------------------------------------------
    # EXAM TIME
    # -----------------------------------------------------

    time_map = {
        20: 30,
        40: 60,
        60: 90,
        100: 120
    }


    exam_minutes = time_map.get(
        selected_question_count,
        60
    )


    # -----------------------------------------------------
    # RENDER EXAM
    # -----------------------------------------------------

    return render_template(
        "jamb/exam.html",
        questions=final_questions,
        subjects=selected_subjects,
        question_count=len(final_questions),
        exam_minutes=exam_minutes
    )


# =========================================================
# JAMB SUBMIT EXAM
# =========================================================
# THERE IS NO RESULT PAGE.
#
# The student's answers are:
#
# 1. Marked automatically
# 2. Score calculated
# 3. Attempt saved
# 4. Student redirected to History
# =========================================================

@app.route(
    "/exam-preparation/jamb/results",
    methods=["POST"]
)
@login_required
def jamb_results():

    question_ids = session.get(
        "jamb_question_ids",
        []
    )


    # -----------------------------------------------------
    # NO ACTIVE EXAM
    # -----------------------------------------------------

    if not question_ids:

        return redirect(
            url_for("exam_preparation")
        )


    # -----------------------------------------------------
    # GET QUESTIONS
    # -----------------------------------------------------

    questions = JAMBQuestion.query.filter(
        JAMBQuestion.id.in_(question_ids)
    ).all()


    question_map = {
        question.id: question
        for question in questions
    }


    ordered_questions = [
        question_map[question_id]
        for question_id in question_ids
        if question_id in question_map
    ]


    # -----------------------------------------------------
    # MARK ANSWERS
    # -----------------------------------------------------

    correct_answers = 0


    for question in ordered_questions:

        submitted_answer = request.form.get(
            f"question_{question.id}"
        )


        if submitted_answer:

            submitted_answer = (
                submitted_answer
                .upper()
                .strip()
            )


            correct_answer = (
                question.correct_answer
                .upper()
                .strip()
            )


            if submitted_answer == correct_answer:

                correct_answers += 1


    # -----------------------------------------------------
    # TOTAL QUESTIONS
    # -----------------------------------------------------

    total_questions = len(
        ordered_questions
    )


    # -----------------------------------------------------
    # CALCULATE SCORE
    # -----------------------------------------------------

    if total_questions > 0:

        percentage = int(
            (
                correct_answers
                /
                total_questions
            )
            * 100
        )

    else:

        percentage = 0


    # -----------------------------------------------------
    # GET START TIME
    # -----------------------------------------------------

    started_at = datetime.utcnow()


    stored_started_at = session.get(
        "jamb_started_at"
    )


    if stored_started_at:

        try:

            started_at = datetime.fromisoformat(
                stored_started_at
            )

        except (ValueError, TypeError):

            started_at = datetime.utcnow()


    # -----------------------------------------------------
    # SAVE ATTEMPT
    # -----------------------------------------------------

    attempt = JAMBExamAttempt(

        student_id=session["student_id"],

        subjects=json.dumps(
            session.get(
                "jamb_subjects",
                []
            )
        ),

        year=None,

        total_questions=total_questions,

        correct_answers=correct_answers,

        score=percentage,

        started_at=started_at,

        completed_at=datetime.utcnow()
    )


    db.session.add(
        attempt
    )


    db.session.commit()


    # -----------------------------------------------------
    # SAVE LAST ATTEMPT
    # -----------------------------------------------------

    session["jamb_last_attempt_id"] = attempt.id


    # -----------------------------------------------------
    # CLEAR CURRENT EXAM
    # -----------------------------------------------------

    session.pop(
        "jamb_question_ids",
        None
    )


    session.pop(
        "jamb_started_at",
        None
    )


    # -----------------------------------------------------
    # IMPORTANT:
    # NO RESULT PAGE
    #
    # Redirect directly to HISTORY.
    # -----------------------------------------------------

    return redirect(
        url_for("jamb_history")
    )


# =========================================================
# JAMB HISTORY
# =========================================================

@app.route(
    "/exam-preparation/jamb/history"
)
@login_required
def jamb_history():

    attempts = JAMBExamAttempt.query.filter_by(
        student_id=session["student_id"]
    ).order_by(
        JAMBExamAttempt.id.desc()
    ).all()


    return render_template(
        "jamb/history.html",
        attempts=attempts
    )


# =========================================================
# JAMB QUESTION BANK
# =========================================================

@app.route(
    "/exam-preparation/jamb/question-bank"
)
@login_required
def jamb_question_bank():

    total_questions = JAMBQuestion.query.count()


    subjects = db.session.query(
        JAMBQuestion.subject
    ).distinct().order_by(
        JAMBQuestion.subject.asc()
    ).all()


    subject_counts = []


    for row in subjects:

        subject_name = row[0]


        count = JAMBQuestion.query.filter_by(
            subject=subject_name
        ).count()


        subject_counts.append({
            "subject": subject_name,
            "count": count
        })


    return render_template(
        "jamb/question-bank.html",
        total_questions=total_questions,
        subject_counts=subject_counts
    )


# =========================================================
# CAREER DEVELOPMENT
# =========================================================

@app.route(
    "/courses/career-development"
)
@login_required
def career_development():

    return render_template(
        "career-development.html"
    )


# =========================================================
# AI ASSISTANT
# =========================================================

@app.route("/ai-assistant")
@login_required
def ai_assistant():

    return render_template(
        "ai-assistant.html"
    )


# =========================================================
# AI MEMORY GET
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
# AI MEMORY SAVE
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


    student.subjects = str(
        data.get(
            "subjects",
            ""
        )
    ).strip()


    student.skills = str(
        data.get(
            "skills",
            ""
        )
    ).strip()


    student.interests = str(
        data.get(
            "interests",
            ""
        )
    ).strip()


    student.career_goal = str(
        data.get(
            "career_goal",
            ""
        )
    ).strip()


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

    opportunities_list = [

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


    return render_template(
        "opportunities.html",
        opportunities=opportunities_list
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
# DATABASE SETUP
# =========================================================

with app.app_context():

    db.create_all()


# =========================================================
# DATABASE MIGRATION
# =========================================================

with app.app_context():

    try:

        inspector = inspect(
            db.engine
        )


        table_names = inspector.get_table_names()


        # -------------------------------------------------
        # JAMB QUESTION TABLE
        # -------------------------------------------------

        if "jamb_question" in table_names:

            columns = inspector.get_columns(
                "jamb_question"
            )


            existing_columns = {
                column["name"]
                for column in columns
            }


            jamb_question_columns = {

                "year": """
                    ALTER TABLE jamb_question
                    ADD COLUMN year INTEGER
                """,

                "topic": """
                    ALTER TABLE jamb_question
                    ADD COLUMN topic VARCHAR(150)
                """,

                "subtopic": """
                    ALTER TABLE jamb_question
                    ADD COLUMN subtopic VARCHAR(150)
                """,

                "difficulty": """
                    ALTER TABLE jamb_question
                    ADD COLUMN difficulty VARCHAR(30)
                """,

                "source": """
                    ALTER TABLE jamb_question
                    ADD COLUMN source VARCHAR(200)
                """,

                "created_at": """
                    ALTER TABLE jamb_question
                    ADD COLUMN created_at TIMESTAMP
                """
            }


            for column_name, sql_statement in jamb_question_columns.items():

                if column_name not in existing_columns:

                    try:

                        with db.engine.begin() as connection:

                            connection.execute(
                                text(
                                    sql_statement
                                )
                            )


                        print(
                            f"JAMB column added: {column_name}"
                        )


                    except Exception as migration_error:

                        print(
                            f"Could not add JAMB column "
                            f"{column_name}:",
                            migration_error
                        )


        # -------------------------------------------------
        # JAMB EXAM ATTEMPT TABLE
        # -------------------------------------------------

        if "jamb_exam_attempt" in table_names:

            columns = inspector.get_columns(
                "jamb_exam_attempt"
            )


            existing_columns = {
                column["name"]
                for column in columns
            }


            if "year" not in existing_columns:

                try:

                    with db.engine.begin() as connection:

                        connection.execute(
                            text(
                                """
                                ALTER TABLE jamb_exam_attempt
                                ADD COLUMN year INTEGER
                                """
                            )
                        )


                    print(
                        "JAMB attempt year column added."
                    )


                except Exception as migration_error:

                    print(
                        "Could not add JAMB attempt year column:",
                        migration_error
                    )


    except Exception as error:

        print(
            "JAMB database migration check failed:",
            error
        )


# =========================================================
# AUTOMATIC JAMB QUESTION SEEDING
# =========================================================

with app.app_context():

    try:

        from seed_jamb import seed_questions


        print(
            "Checking Career Bridge JAMB question bank..."
        )


        seed_questions()


        total_jamb_questions = JAMBQuestion.query.count()


        print(
            f"JAMB question bank ready: "
            f"{total_jamb_questions} questions."
        )


    except ModuleNotFoundError:

        print(
            "seed_jamb.py was not found. "
            "JAMB questions were not automatically seeded."
        )


    except Exception as seed_error:

        db.session.rollback()


        print(
            "Automatic JAMB question seeding failed:",
            seed_error
        )


# =========================================================
# CREATE ADMIN ACCOUNT
# =========================================================

with app.app_context():

    admin_username = os.environ.get(
        "ADMIN_USERNAME"
    )


    admin_password = os.environ.get(
        "ADMIN_PASSWORD"
    )


    if admin_username and admin_password:

        existing_admin = Admin.query.filter_by(
            username=admin_username
        ).first()


        if not existing_admin:

            admin = Admin(
                username=admin_username,
                password=generate_password_hash(
                    admin_password
                )
            )


            db.session.add(
                admin
            )


            db.session.commit()


            print(
                "Admin account created successfully."
            )


# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
