from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime
import os

app = Flask(__name__)

app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "career-bridge-development-key"
)

database_url = os.environ.get("DATABASE_URL")
if not database_url:
    raise RuntimeError("DATABASE_URL is not set.")

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    subjects = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    interests = db.Column(db.Text, nullable=True)
    career_goal = db.Column(db.Text, nullable=True)


class Mentor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(150), nullable=False)
    field = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(120), nullable=True)
    verified = db.Column(db.Boolean, default=False)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class MentorshipRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    mentor_id = db.Column(db.Integer, db.ForeignKey("mentor.id"), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Pending", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("Student", backref=db.backref("mentorship_requests", lazy=True))
    mentor = db.relationship("Mentor", backref=db.backref("mentorship_requests", lazy=True))


# New table: stores each student's Digital Skills progress.
class DigitalSkillsProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("student.id"), nullable=False)
    module = db.Column(db.Integer, nullable=False)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    quiz_score = db.Column(db.Integer, nullable=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    student = db.relationship(
        "Student",
        backref=db.backref("digital_skills_progress", lazy=True)
    )

    __table_args__ = (
        db.UniqueConstraint("student_id", "module", name="unique_student_digital_module"),
    )


TOTAL_DIGITAL_MODULES = 10


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "student_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_id" not in session:
            return redirect(url_for("admin_login"))
        return f(*args, **kwargs)
    return decorated_function


def get_digital_progress(student_id):
    completed = DigitalSkillsProgress.query.filter_by(
        student_id=student_id,
        completed=True
    ).count()

    percentage = round((completed / TOTAL_DIGITAL_MODULES) * 100)
    return completed, TOTAL_DIGITAL_MODULES, percentage


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            return "Please fill in all fields."

        if Student.query.filter_by(email=email).first():
            return "An account with this email already exists."

        student = Student(
            name=name,
            email=email,
            password=generate_password_hash(password)
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
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

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
    session.pop("student_id", None)
    session.pop("student_name", None)
    return redirect(url_for("login"))


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        admin = Admin.query.filter_by(username=username).first()
        if not admin:
            return "Admin account not found."

        if not check_password_hash(admin.password, password):
            return "Incorrect admin password."

        session["admin_id"] = admin.id
        session["admin_username"] = admin.username
        return redirect(url_for("admin_dashboard"))

    return render_template("admin-login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    session.pop("admin_username", None)
    return redirect(url_for("admin_login"))


@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():
    mentors_count = Mentor.query.count()
    requests_count = MentorshipRequest.query.count()
    pending_requests = MentorshipRequest.query.filter_by(status="Pending").count()
    return render_template(
        "admin-dashboard.html",
        mentors_count=mentors_count,
        requests_count=requests_count,
        pending_requests=pending_requests
    )


@app.route("/add-mentor", methods=["GET", "POST"])
@admin_required
def add_mentor():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        profession = request.form.get("profession", "").strip()
        field = request.form.get("field", "").strip()
        bio = request.form.get("bio", "").strip()
        skills = request.form.get("skills", "").strip()
        experience = request.form.get("experience", "").strip()
        email = request.form.get("email", "").strip()

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
        return redirect(url_for("mentors"))

    return render_template("add-mentor.html")


@app.route("/admin/delete-mentor/<int:mentor_id>", methods=["POST"])
@admin_required
def delete_mentor(mentor_id):
    mentor = Mentor.query.get_or_404(mentor_id)
    MentorshipRequest.query.filter_by(mentor_id=mentor.id).delete()
    db.session.delete(mentor)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))


@app.route("/mentors")
@login_required
def mentors():
    mentors_list = Mentor.query.filter_by(verified=True).order_by(Mentor.name.asc()).all()
    return render_template("mentors.html", mentors=mentors_list)


@app.route("/mentor/<int:mentor_id>")
@login_required
def mentor_profile(mentor_id):
    mentor = Mentor.query.get_or_404(mentor_id)
    if not mentor.verified:
        return "Mentor not available.", 404
    return render_template("mentor-profile.html", mentor=mentor)


@app.route("/mentor/<int:mentor_id>/request", methods=["GET", "POST"])
@login_required
def request_mentorship(mentor_id):
    mentor = Mentor.query.get_or_404(mentor_id)
    if not mentor.verified:
        return "Mentor not available.", 404

    if request.method == "POST":
        message = request.form.get("message", "").strip()
        if not message:
            return "Please enter a message."

        mentorship_request = MentorshipRequest(
            student_id=session["student_id"],
            mentor_id=mentor.id,
            message=message,
            status="Pending"
        )
        db.session.add(mentorship_request)
        db.session.commit()
        return redirect(url_for("my_mentorship_requests"))

    return render_template("request-mentorship.html", mentor=mentor)


@app.route("/my-mentorship-requests")
@login_required
def my_mentorship_requests():
    requests = MentorshipRequest.query.filter_by(
        student_id=session["student_id"]
    ).order_by(MentorshipRequest.id.desc()).all()
    return render_template("my-mentorship-requests.html", requests=requests)


@app.route("/admin/mentorship-requests")
@admin_required
def admin_mentorship_requests():
    requests = MentorshipRequest.query.order_by(MentorshipRequest.id.desc()).all()
    return render_template("admin-mentorship-requests.html", requests=requests)


@app.route("/admin/mentorship-request/<int:request_id>/<status>", methods=["POST"])
@admin_required
def update_mentorship_request(request_id, status):
    allowed_statuses = ["Pending", "Accepted", "Declined"]
    if status not in allowed_statuses:
        return "Invalid status.", 400

    mentorship_request = MentorshipRequest.query.get_or_404(request_id)
    mentorship_request.status = status
    db.session.commit()
    return redirect(url_for("admin_mentorship_requests"))


@app.route("/dashboard")
@login_required
def dashboard():
    completed, total, percentage = get_digital_progress(session["student_id"])
    mentorship_requests = MentorshipRequest.query.filter_by(
        student_id=session["student_id"]
    ).order_by(MentorshipRequest.id.desc()).limit(3).all()

    return render_template(
        "dashboard.html",
        digital_completed=completed,
        digital_total=total,
        digital_percentage=percentage,
        mentorship_requests=mentorship_requests
    )


@app.route("/certificate")
@login_required
def certificate():
    digital_completed, digital_total, digital_percentage = get_digital_progress(session["student_id"])
    return render_template(
        "certificate.html",
        digital_completed=digital_completed,
        digital_total=digital_total,
        digital_percentage=digital_percentage
    )


@app.route("/about")
@login_required
def about():
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


# Python course
@app.route("/courses/python")
@login_required
def python():
    return render_template("python.html")


for number in range(1, 11):
    def make_python_route(module_number):
        @app.route(f"/python/module{module_number}")
        @login_required
        def python_module():
            return render_template(f"python/module{module_number}.html")
        python_module.__name__ = f"python_module{module_number}"
        return python_module
    make_python_route(number)


# CV + LinkedIn course
@app.route("/courses/cv-linkedin")
@login_required
def cv_linkedin():
    return render_template("cv-linkedin.html")


for number in range(1, 6):
    def make_cv_route(module_number):
        @app.route(f"/cv-linkedin/module{module_number}")
        @login_required
        def cv_module():
            return render_template(f"cv-linkedin/module{module_number}.html")
        cv_module.__name__ = f"cv_linkedin_module{module_number}"
        return cv_module
    make_cv_route(number)


# =========================================================
# DIGITAL SKILLS COURSE + PROGRESS
# =========================================================

@app.route("/courses/digital-skills")
@login_required
def digital_skills():
    completed, total, percentage = get_digital_progress(session["student_id"])
    return render_template(
        "digital-skills.html",
        digital_completed=completed,
        digital_total=total,
        digital_percentage=percentage
    )


for number in range(1, TOTAL_DIGITAL_MODULES + 1):
    def make_digital_route(module_number):
        @app.route(f"/digital-skills/module{module_number}")
        @login_required
        def digital_module():
            progress = DigitalSkillsProgress.query.filter_by(
                student_id=session["student_id"],
                module=module_number
            ).first()
            return render_template(
                f"digital-skills/module{module_number}.html",
                module_number=module_number,
                progress=progress
            )
        digital_module.__name__ = f"digital_skills_module{module_number}"
        return digital_module
    make_digital_route(number)


@app.route("/digital-skills/module/<int:module_number>/complete", methods=["POST"])
@login_required
def complete_digital_module(module_number):
    if module_number < 1 or module_number > TOTAL_DIGITAL_MODULES:
        return "Invalid module.", 404

    record = DigitalSkillsProgress.query.filter_by(
        student_id=session["student_id"],
        module=module_number
    ).first()

    if not record:
        record = DigitalSkillsProgress(
            student_id=session["student_id"],
            module=module_number
        )
        db.session.add(record)

    record.completed = True
    record.completed_at = datetime.utcnow()

    score = request.form.get("quiz_score")
    if score is not None and str(score).strip() != "":
        try:
            record.quiz_score = max(0, min(100, int(score)))
        except ValueError:
            pass

    db.session.commit()
    return redirect(url_for("digital_skills_progress"))


@app.route("/digital-skills/progress")
@login_required
def digital_skills_progress():
    progress_records = DigitalSkillsProgress.query.filter_by(
        student_id=session["student_id"]
    ).order_by(DigitalSkillsProgress.module.asc()).all()

    completed, total, percentage = get_digital_progress(session["student_id"])
    completed_modules = {record.module for record in progress_records if record.completed}

    return render_template(
        "digital-skills-progress.html",
        progress_records=progress_records,
        completed_modules=completed_modules,
        digital_completed=completed,
        digital_total=total,
        digital_percentage=percentage
    )


@app.route("/api/digital-skills/progress")
@login_required
def api_digital_skills_progress():
    completed, total, percentage = get_digital_progress(session["student_id"])
    records = DigitalSkillsProgress.query.filter_by(
        student_id=session["student_id"]
    ).order_by(DigitalSkillsProgress.module.asc()).all()

    return jsonify({
        "success": True,
        "completed": completed,
        "total": total,
        "percentage": percentage,
        "modules": [
            {
                "module": record.module,
                "completed": record.completed,
                "quiz_score": record.quiz_score
            }
            for record in records
        ]
    })


@app.route("/courses/career-development")
@login_required
def career_development():
    return render_template("career-development.html")


@app.route("/ai-assistant")
@login_required
def ai_assistant():
    return render_template("ai-assistant.html")


@app.route("/api/ai-memory", methods=["GET"])
@login_required
def get_ai_memory():
    student = Student.query.get(session["student_id"])
    if not student:
        return jsonify({"success": False, "message": "Student not found."}), 404

    return jsonify({
        "success": True,
        "memory": {
            "subjects": student.subjects or "",
            "skills": student.skills or "",
            "interests": student.interests or "",
            "career_goal": student.career_goal or ""
        }
    })


@app.route("/api/ai-memory", methods=["POST"])
@login_required
def save_ai_memory():
    student = Student.query.get(session["student_id"])
    if not student:
        return jsonify({"success": False, "message": "Student not found."}), 404

    data = request.get_json(silent=True) or {}
    student.subjects = str(data.get("subjects", "")).strip()
    student.skills = str(data.get("skills", "")).strip()
    student.interests = str(data.get("interests", "")).strip()
    student.career_goal = str(data.get("career_goal", "")).strip()
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


@app.route("/library")
@login_required
def library():
    return render_template("library.html")


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
    return render_template("opportunities.html", opportunities=opportunities_list)


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

    admin_username = os.environ.get("ADMIN_USERNAME")
    admin_password = os.environ.get("ADMIN_PASSWORD")

    if admin_username and admin_password:
        existing_admin = Admin.query.filter_by(username=admin_username).first()
        if not existing_admin:
            admin = Admin(
                username=admin_username,
                password=generate_password_hash(admin_password)
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin account created successfully.")


if __name__ == "__main__":
    app.run(debug=True)
