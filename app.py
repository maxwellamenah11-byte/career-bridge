from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>Career Bridge</title>

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        html {
            scroll-behavior: smooth;
        }

        body {
            font-family: Arial, sans-serif;
            background: #020617;
            color: #e2e8f0;
        }


        /* NAVIGATION */

        nav {
            background: #020617;
            padding: 18px 7%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
            border-bottom: 1px solid #1e293b;
        }

        nav h2 {
            color: white;
            font-size: 24px;
        }

        .menu-button {
            background: #2563eb;
            color: white;
            border: none;
            padding: 12px 18px;
            border-radius: 8px;
            font-size: 15px;
            cursor: pointer;
        }

        .menu-button:hover {
            background: #1d4ed8;
        }

        .nav-menu {
            display: none;
            position: absolute;
            right: 7%;
            top: 70px;
            width: 190px;
            background: #0f172a;
            padding: 10px;
            border-radius: 10px;
            border: 1px solid #1e293b;
            box-shadow: 0 10px 30px rgba(0,0,0,0.4);
        }

        .nav-menu.show {
            display: block;
        }

        .nav-menu a {
            display: block;
            color: white;
            text-decoration: none;
            padding: 13px 15px;
            border-radius: 7px;
        }

        .nav-menu a:hover {
            background: #2563eb;
        }


        /* HERO */

        .hero {
            min-height: 85vh;
            padding: 70px 8%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(135deg, #020617, #0f172a, #172554);
        }

        .hero h1 {
            font-size: 62px;
            color: #60a5fa;
            margin-bottom: 20px;
        }

        .hero h3 {
            font-size: 27px;
            color: white;
            margin-bottom: 20px;
        }

        .hero p {
            max-width: 700px;
            font-size: 18px;
            line-height: 1.8;
            color: #cbd5e1;
            margin-bottom: 30px;
        }


        /* BUTTONS */

        .button {
            display: inline-block;
            background: #2563eb;
            color: white;
            padding: 14px 25px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            margin: 5px;
        }

        .button:hover {
            background: #1d4ed8;
        }


        /* GENERAL SECTIONS */

        section {
            padding: 80px 8%;
        }

        section h2 {
            text-align: center;
            font-size: 38px;
            margin-bottom: 20px;
            color: white;
        }

        .section-intro {
            text-align: center;
            max-width: 700px;
            margin: 0 auto 45px;
            line-height: 1.7;
            color: #94a3b8;
        }


        /* ABOUT */

        .about {
            background: #0f172a;
            text-align: center;
        }

        .about p {
            max-width: 800px;
            margin: auto;
            line-height: 1.9;
            font-size: 17px;
            color: #cbd5e1;
        }

        .about strong {
            color: #60a5fa;
        }


        /* SERVICES */

        .services {
            background: #020617;
        }

        .cards {
            display: flex;
            justify-content: center;
            gap: 25px;
            flex-wrap: wrap;
        }

        .card {
            background: #0f172a;
            width: 270px;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #1e293b;
            text-align: center;
            transition: 0.3s;
        }

        .card:hover {
            transform: translateY(-6px);
            border-color: #2563eb;
        }

        .card .icon {
            font-size: 40px;
            margin-bottom: 15px;
        }

        .card h3 {
            color: #60a5fa;
            margin-bottom: 15px;
        }

        .card p {
            line-height: 1.7;
            color: #94a3b8;
        }


        /* COURSES */

        .courses {
            background: #0f172a;
        }

        .course {
            background: #020617;
            width: 280px;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #1e293b;
        }

        .course h3 {
            margin-bottom: 12px;
            color: #60a5fa;
        }

        .course p {
            line-height: 1.7;
            margin-bottom: 15px;
            color: #94a3b8;
        }


        /* CONTACT */

        .contact {
            background: #172554;
            text-align: center;
        }

        .contact-options {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 35px;
        }

        .contact-box {
            background: #0f172a;
            width: 280px;
            padding: 30px;
            border-radius: 12px;
            border: 1px solid #1e293b;
        }

        .contact-box h3 {
            margin-bottom: 15px;
            color: white;
        }

        .contact-box p {
            margin-bottom: 20px;
            color: #94a3b8;
            line-height: 1.6;
        }


        /* SOCIAL */

        .social {
            background: #020617;
            text-align: center;
        }

        .social a {
            display: inline-block;
            margin: 10px;
            padding: 13px 22px;
            background: #0f172a;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            border: 1px solid #1e293b;
        }

        .social a:hover {
            background: #2563eb;
        }


        /* FOOTER */

        footer {
            background: #020617;
            color: #94a3b8;
            text-align: center;
            padding: 30px;
            border-top: 1px solid #1e293b;
        }

        footer p {
            margin: 7px;
        }


        /* MOBILE */

        @media (max-width: 700px) {

            nav {
                padding: 16px 5%;
            }

            .nav-menu {
                right: 5%;
            }

            .hero {
                min-height: 80vh;
                padding: 60px 5%;
            }

            .hero h1 {
                font-size: 44px;
            }

            .hero h3 {
                font-size: 22px;
            }

            .hero p {
                font-size: 16px;
            }

            section {
                padding: 60px 5%;
            }

            section h2 {
                font-size: 31px;
            }

        }

    </style>

</head>


<body>


<!-- NAVIGATION -->

<nav>

    <h2>Career Bridge</h2>

    <button class="menu-button" onclick="toggleMenu()">
        ☰ Navigate
    </button>

    <div class="nav-menu" id="navMenu">

        <a href="#home" onclick="toggleMenu()">🏠 Home</a>

        <a href="#about" onclick="toggleMenu()">👤 About</a>

        <a href="#services" onclick="toggleMenu()">💼 Services</a>

        <a href="#courses" onclick="toggleMenu()">📚 Courses</a>

        <a href="#contact" onclick="toggleMenu()">📞 Contact</a>

    </div>

</nav>


<!-- HOME -->

<section class="hero" id="home">

    <h1>Career Bridge</h1>

    <h3>Build Skills. Build Your Future.</h3>

    <p>
        Career Bridge helps students develop practical skills,
        create professional CVs and prepare for future career
        opportunities.
    </p>

    <div>

        <a href="#services" class="button">
            Explore Services
        </a>

        <a href="#contact" class="button">
            Contact Me
        </a>

    </div>

</section>


<!-- ABOUT -->

<section class="about" id="about">

    <h2>About Career Bridge</h2>

    <p>

        Career Bridge is a platform designed to help students
        prepare for the world of work before graduation.

        We focus on practical skills, career development,
        CV preparation and useful online learning opportunities.

        Our goal is simple:

        <strong>
            to help students build skills today for the
            opportunities of tomorrow.
        </strong>

    </p>

</section>


<!-- SERVICES -->

<section class="services" id="services">

    <h2>Career Services</h2>

    <p class="section-intro">

        We provide practical services designed to help students
        become more confident and career-ready.

    </p>


    <div class="cards">


        <div class="card">

            <div class="icon">📄</div>

            <h3>CV Creation</h3>

            <p>

                Get help creating a professional CV that
                highlights your education, skills, certificates
                and experience.

            </p>

        </div>


        <div class="card">

            <div class="icon">🐍</div>

            <h3>Python Training</h3>

            <p>

                Learn the fundamentals of Python programming
                and begin developing your digital skills.

            </p>

        </div>


        <div class="card">

            <div class="icon">🧭</div>

            <h3>Career Guidance</h3>

            <p>

                Get guidance on career choices, useful skills
                and preparing for opportunities after school.

            </p>

        </div>


        <div class="card">

            <div class="icon">💼</div>

            <h3>Career Preparation</h3>

            <p>

                Learn how to present yourself professionally
                and prepare for future internships and jobs.

            </p>

        </div>


    </div>

</section>


<!-- COURSES -->

<section class="courses" id="courses">

    <h2>Skills & Courses</h2>

    <p class="section-intro">

        Learn useful skills that can strengthen your knowledge,
        confidence and future CV.

    </p>


    <div class="cards">


        <div class="course">

            <h3>Python Programming</h3>

            <p>

                Learn Python from the basics and build
                simple projects.

            </p>

            <a href="#contact" class="button">
                Learn More
            </a>

        </div>


        <div class="course">

            <h3>CV & LinkedIn</h3>

            <p>

                Learn how to create a strong CV and develop
                a professional LinkedIn presence.

            </p>

            <a href="#contact" class="button">
                Learn More
            </a>

        </div>


        <div class="course">

            <h3>Digital Skills</h3>

            <p>

                Develop useful computer and digital skills
                for school and future work.

            </p>

            <a href="#contact" class="button">
                Learn More
            </a>

        </div>


        <div class="course">

            <h3>Career Development</h3>

            <p>

                Learn how to plan your career and identify
                skills that can help you grow.

            </p>

            <a href="#contact" class="button">
                Learn More
            </a>

        </div>


    </div>

</section>


<!-- CONTACT -->

<section class="contact" id="contact">

    <h2>Reach Career Bridge</h2>

    <p class="section-intro">

        Have a question or interested in our services?
        You can reach us through any of the options below.

    </p>


    <div class="contact-options">


        <div class="contact-box">

            <h3>📧 Email</h3>

            <p>

                Send an email for enquiries,
                business questions and collaborations.

            </p>

            <a
                href="mailto:maxwellamenah11@gmail.com"
                class="button">

                Send Email

            </a>

        </div>


        <div class="contact-box">

            <h3>💬 WhatsApp</h3>

            <p>

                Chat directly with Career Bridge
                on WhatsApp.

            </p>

            <a
                href="https://wa.me/2349026832566"
                target="_blank"
                class="button">

                Chat on WhatsApp

            </a>

        </div>


    </div>

</section>


<!-- SOCIAL MEDIA -->

<section class="social">

    <h2>Follow Career Bridge</h2>

    <p class="section-intro">

        Follow us for career tips, learning opportunities
        and useful student content.

    </p>


    <a
        href="https://www.tiktok.com/@maxwellamenah"
        target="_blank">

        🎵 TikTok

    </a>


    <a href="mailto:maxwellamenah11@gmail.com">

        📧 Email

    </a>


    <a
        href="https://wa.me/2349026832566"
        target="_blank">

        💬 WhatsApp

    </a>

</section>


<!-- FOOTER -->

<footer>

    <p>
        <strong>Career Bridge</strong>
    </p>

    <p>
        Building skills. Connecting opportunities.
    </p>

    <p>
        © 2026 Career Bridge. All rights reserved.
    </p>

</footer>


<script>

function toggleMenu() {

    document
        .getElementById("navMenu")
        .classList
        .toggle("show");

}

</script>


</body>

</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
