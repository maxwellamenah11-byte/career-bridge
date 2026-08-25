from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/about")
def about():
    return render_template("about.html")


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


@app.route("/courses/cv-linkedin")
def cv_linkedin():
    return render_template("cv-linkedin.html")


@app.route("/courses/digital-skills")
def digital_skills():
    return render_template("digital-skills.html")


@app.route("/courses/career-development")
def career_development():
    return render_template("career-development.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/resources")
def resources():
    return render_template("resources.html")


@app.route("/opportunities")
def opportunities():
    return render_template("opportunities.html")


@app.route("/career-explorer")
def career_explorer():
    return render_template("career-explorer.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


if __name__ == "__main__":
