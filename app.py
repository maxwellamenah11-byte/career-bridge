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


@app.route("/career-quiz")
def career_quiz():
    return render_template("career-quiz.html")


@app.route("/cv-builder")
def cv_builder():
    return render_template("cv-builder.html")


if __name__ == "__main__":
    app.run(debug=True)
