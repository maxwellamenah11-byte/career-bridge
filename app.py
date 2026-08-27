from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


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
            "title": "Student Scholarship Programme",
            "organization": "Career Bridge",
            "category": "Scholarships",
            "description": "A sample scholarship opportunity for students seeking financial support for their education.",
            "deadline": "30 September 2026",
            "location": "Nigeria",
            "type": "Scholarship",
            "link": "#"
        },

        {
            "title": "Technology Internship Programme",
            "organization": "Career Bridge",
            "category": "Internships",
            "description": "A sample internship opportunity designed to help students gain practical technology experience.",
            "deadline": "15 October 2026",
            "location": "Nigeria",
            "type": "Internship",
            "link": "#"
        },

        {
            "title": "Student Innovation Challenge",
            "organization": "Career Bridge",
            "category": "Competitions",
            "description": "A sample competition where students can develop ideas and showcase their creativity.",
            "deadline": "20 October 2026",
            "location": "Online",
            "type": "Competition",
            "link": "#"
        },

        {
            "title": "Digital Skills Training",
            "organization": "Career Bridge",
            "category": "Free Courses",
            "description": "A sample learning programme focused on developing practical digital skills.",
            "deadline": "Open",
            "location": "Online",
            "type": "Training",
            "link": "/courses"@app.route("/opportunities")
def opportunities():

    opportunities = [

        {
            "title": "Student Scholarship Programme",
            "organization": "Career Bridge",
            "category": "Scholarships",
            "description": "A sample scholarship opportunity for students seeking financial support for their education.",
            "deadline": "30 September 2026",
            "location": "Nigeria",
            "type": "Scholarship",
            "link": "#"
        },

        {
            "title": "Technology Internship Programme",
            "organization": "Career Bridge",
            "category": "Internships",
            "description": "A sample internship opportunity designed to help students gain practical technology experience.",
            "deadline": "15 October 2026",
            "location": "Nigeria",
            "type": "Internship",
            "link": "#"
        },

        {
            "title": "Student Innovation Challenge",
            "organization": "Career Bridge",
            "category": "Competitions",
            "description": "A sample competition where students can develop ideas and showcase their creativity.",
            "deadline": "20 October 2026",
            "location": "Online",
            "type": "Competition",
            "link": "#"
        },

        {
            "title": "Digital Skills Training",
            "organization": "Career Bridge",
            "category": "Free Courses",
            "description": "A sample learning programme focused on developing practical digital skills.",
            "deadline": "Open",
            "location": "Online",
            "type": "Training",
            "link": "/courses"
        },

        {
            "title": "Youth Volunteer Programme",
            "organization": "Career Bridge",
            "category": "Volunteering",
            "description": "A sample volunteer programme designed to help young people gain experience and contribute to their communities.",
            "deadline": "Open",
            "location": "Nigeria",
            "type": "Volunteer",
            "link": "#"
        },

        {
            "title": "Career Development Programme",
            "organization": "Career Bridge",
            "category": "Career Programmes",
            "description": "A sample programme focused on career preparation, professional skills and workplace readiness.",
            "deadline": "10 November 2026",
            "location": "Online",
            "type": "Career Programme",
            "link": "#"
        }

    ]

    return render_template(
        "opportunities.html",
        opportunities=opportunities
    )
        },

        {
            "title": "Youth Volunteer Programme",
            "organization": "Career Bridge",
            "category": "Volunteering",
            "description": "A sample volunteer programme designed to help young people gain experience and contribute to their communities.",
            "deadline": "Open",
            "location": "Nigeria",
            "type": "Volunteer",
            "link": "#"
        },

        {
            "title": "Career Development Programme",
            "organization": "Career Bridge",
            "category": "Career Programmes",
            "description": "A sample programme focused on career preparation, professional skills and workplace readiness.",
            "deadline": "10 November 2026",
            "location": "Online",
            "type": "Career Programme",
            "link": "#"
        }

    ]

    return render_template(
        "opportunities.html",
        opportunities=opportunities
    )
]


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


if __name__ == "__main__":
    app.run(debug=True)
