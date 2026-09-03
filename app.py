from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
from sqlalchemy import inspect, text
import os
import json
import requests


# =========================================================
# APP SETUP
# =========================================================

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "career-bridge-development-key"
)

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
# JAMB API SETTINGS
# =========================================================

ALOC_API_URL = "https://questions.aloc.com.ng/api/v2/q"

ALOC_ACCESS_TOKEN = os.environ.get(
    "ALOC_ACCESS_TOKEN"
)


# =========================================================
# FETCH JAMB QUESTIONS FROM ALOC
# =========================================================

def fetch_jamb_questions_from_api(
    subject,
    year,
    limit=40
):

    if not ALOC_ACCESS_TOKEN:
        print(
            "ALOC_ACCESS_TOKEN is not configured."
        )
        return []

    params = {
        "subject": subject.lower(),
        "year": year,
        "type": "utme"
    }

    headers = {
        "AccessToken": ALOC_ACCESS_TOKEN
    }

    try:

        response = requests.get(
            ALOC_API_URL,
            params=params,
            headers=headers,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        # Some API responses return the question
        # directly while others return a data list.

        if isinstance(data, dict):

            if "data" in data:
                data = data["data"]

            elif "questions" in data:
                data = data["questions"]

        if isinstance(data, dict):
            data = [data]

        if not isinstance(data, list):
            return []

        return data[:limit]

    except requests.RequestException as error:

        print(
            "ALOC API request failed:",
            error
        )

        return []

    except ValueError as error:

        print(
            "ALOC API returned invalid JSON:",
            error
        )

        return []


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

    # NEW: QUESTION YEAR
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
# STUDENT REGISTER
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
            return "Please fill in all fields."

        existing_student = Student.query.filter_by(
            email=email
        ).first()

        if existing_student:
            return "An account with this email already exists."

        student = Student(
            name=name,
            email=email,
            password=generate_password_hash(
                password
            )
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
# STUDENT LOGIN
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
# STUDENT LOGOUT
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
        "jamb_question_ids",
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
            return "Admin account not found."

        if not check_password_hash(
            admin.password,
            password
        ):
            return "Incorrect admin password."

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
            return "Name, profession and field are required."

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

        db.session.add(mentor)
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

    db.session.delete(mentor)
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
        return "Mentor not available.", 404

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
        return "Mentor not available.", 404

    if request.method == "POST":

        message = request.form.get(
            "message",
            ""
        ).strip()

        if not message:
            return "Please enter a message."

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
# STUDENT MENTORSHIP INBOX
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
# ADMIN MENTORSHIP INBOX
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
# ADMIN UPDATE MENTORSHIP REQUEST
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
        return "Invalid status.", 400

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
# STUDENT DASHBOARD
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
# DIGITAL SKILLS PROGRESS PAGE
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
        return "Invalid module.", 400

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

        db.session.add(record)

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
# DIGITAL SKILLS PROGRESS API
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
        "English",
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

    selected_year = request.form.get(
        "year",
        ""
    ).strip()

    # -----------------------------------------
    # CHECK YEAR
    # -----------------------------------------

    if not selected_year:

        return (
            "Please select an exam year.",
            400
        )

    try:

        selected_year = int(
            selected_year
        )

    except ValueError:

        return (
            "Invalid exam year.",
            400
        )

    # -----------------------------------------
    # CHECK YEAR RANGE
    # -----------------------------------------

    if selected_year < 2000 or selected_year > 2026:

        return (
            "Invalid exam year.",
            400
        )

    # -----------------------------------------
    # CHECK SUBJECTS
    # -----------------------------------------

    if not selected_subjects:

        return (
            "Please select at least one subject.",
            400
        )

    # -----------------------------------------
    # SAVE SELECTION
    # -----------------------------------------

    session["jamb_year"] = selected_year

    session["jamb_subjects"] = selected_subjects

    # Clear any previous exam questions

    session.pop(
        "jamb_question_ids",
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

    selected_year = session.get(
        "jamb_year"
    )

    # -----------------------------------------
    # CHECK SELECTION
    # -----------------------------------------

    if not selected_subjects or not selected_year:

        return redirect(
            url_for("exam_preparation")
        )

    # -----------------------------------------
    # FIND QUESTIONS
    # -----------------------------------------

    questions = JAMBQuestion.query.filter(
        JAMBQuestion.year == selected_year,
        JAMBQuestion.subject.in_(
            selected_subjects
        )
    ).order_by(
        JAMBQuestion.id.asc()
    ).all()

    # -----------------------------------------
    # NO QUESTIONS
    # -----------------------------------------

    if not questions:

        return (
            f"There are currently no JAMB questions "
            f"available for {selected_year} in the "
            f"selected subjects.",
            404
        )

    # -----------------------------------------
    # SAVE QUESTION IDS
    # -----------------------------------------

    session["jamb_question_ids"] = [
        question.id
        for question in questions
    ]

    # -----------------------------------------
    # START TIME
    # -----------------------------------------

    session["jamb_started_at"] = datetime.utcnow().isoformat()

    return render_template(
        "jamb/exam.html",
        questions=questions,
        subjects=selected_subjects,
        year=selected_year
    )


# =========================================================
# JAMB RESULTS
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

    if not question_ids:

        return redirect(
            url_for("exam_preparation")
        )

    questions = JAMBQuestion.query.filter(
        JAMBQuestion.id.in_(question_ids)
    ).all()

    correct_answers = 0

    # -----------------------------------------
    # MARK ANSWERS
    # -----------------------------------------

    for question in questions:

        submitted_answer = request.form.get(
            f"question_{question.id}"
        )

        if submitted_answer:

            if (
                submitted_answer.upper()
                == question.correct_answer.upper()
            ):

                correct_answers += 1

    # -----------------------------------------
    # CALCULATE SCORE
    # -----------------------------------------

    total_questions = len(
        questions
    )

    if total_questions > 0:

        percentage = int(
            (correct_answers / total_questions) * 100
        )

    else:

        percentage = 0

    # -----------------------------------------
    # SAVE ATTEMPT
    # -----------------------------------------

    attempt = JAMBExamAttempt(
        student_id=session["student_id"],

        subjects=json.dumps(
            session.get(
                "jamb_subjects",
                []
            )
        ),

        total_questions=total_questions,

        correct_answers=correct_answers,

        score=percentage,

        completed_at=datetime.utcnow()
    )

    db.session.add(
        attempt
    )

    db.session.commit()

    # -----------------------------------------
    # SAVE LAST ATTEMPT
    # -----------------------------------------

    session["jamb_last_attempt_id"] = attempt.id

    # -----------------------------------------
    # CLEAR ACTIVE EXAM
    # -----------------------------------------

    session.pop(
        "jamb_question_ids",
        None
    )

    session.pop(
        "jamb_started_at",
        None
    )

    return render_template(
        "jamb/results.html",
        attempt=attempt,
        percentage=percentage
    )


# =========================================================
# JAMB ATTEMPT HISTORY
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
# OTHER COURSES
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
#
# The JAMBQuestion model now has a "year" column.
#
# db.create_all() does NOT add new columns to an existing
# table, so this checks whether the column exists and adds
# it if necessary.
#
# =========================================================

with app.app_context():

    try:

        inspector = inspect(db.engine)

        table_names = inspector.get_table_names()

        if "jamb_question" in table_names:

            columns = inspector.get_columns(
                "jamb_question"
            )

            column_names = {
                column["name"]
                for column in columns
            }

            if "year" not in column_names:

                if db.engine.dialect.name == "postgresql":

                    with db.engine.begin() as connection:

                        connection.execute(
                            text(
                                "ALTER TABLE jamb_question "
                                "ADD COLUMN year INTEGER"
                            )
                        )

                    print(
                        "JAMB year column added to PostgreSQL."
                    )

                elif db.engine.dialect.name == "sqlite":

                    with db.engine.begin() as connection:

                        connection.execute(
                            text(
                                "ALTER TABLE jamb_question "
                                "ADD COLUMN year INTEGER"
                            )
                        )

                    print(
                        "JAMB year column added to SQLite."
                    )

    except Exception as error:

        print(
            "JAMB database migration check failed:",
            error
        )


# =========================================================
# CREATE ADMIN ACCOUNT FROM RENDER ENVIRONMENT VARIABLES
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
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )
