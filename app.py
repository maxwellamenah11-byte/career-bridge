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
            background: #f5f7fb;
            color: #1f2937;
        }

        /* NAVIGATION */

        nav {
            background: #111827;
            padding: 20px 8%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        nav h2 {
            color: white;
            font-size: 24px;
        }

        nav a {
            color: white;
            text-decoration: none;
            margin-left: 22px;
            font-size: 15px;
        }

        nav a:hover {
            color: #60a5fa;
        }


        /* HERO */

        .hero {
            min-height: 80vh;
            padding: 60px 8%;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(135deg, #e0ecff, #f5f7fb);
        }

        .hero h1 {
            font-size: 60px;
            color: #1d4ed8;
            margin-bottom: 20px;
        }

        .hero h3 {
            font-size: 26px;
            margin-bottom: 20px;
        }

        .hero p {
            max-width: 700px;
            font-size: 19px;
            line-height: 1.7;
            margin-bottom: 30px;
        }

        .button {
            display: inline-block;
            background: #2563eb;
            color: white;
            padding: 15px 28px;
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
            color: #111827;
        }

        .section-intro {
            text-align: center;
            max-width: 700px;
            margin: 0 auto 45px;
            line-height: 1.7;
        }


        /* ABOUT */

        .about {
            background: white;
            text-align: center;
        }

        .about p {
            max-width: 750px;
            margin: auto;
            line-height: 1.8;
            font-size: 17px;
        }


        /* SERVICES */

        .services {
            background: #f5f7fb;
        }

        .cards {
            display: flex;
            justify-content: center;
            gap: 25px;
            flex-wrap: wrap;
        }

        .card {
            background: white;
            width: 270px;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.08);
            text-align: center;
            transition: 0.3s;
        }

        .card:hover {
            transform: translateY(-5px);
        }

        .card .icon {
            font-size: 40px;
            margin-bottom: 15px;
        }

        .card h3 {
            color: #2563eb;
            margin-bottom: 15px;
        }

        .card p {
            line-height: 1.6;
        }


        /* COURSES */

        .courses {
            background: white;
        }

        .course {
            background: #f8fafc;
            width: 280px;
            padding: 25px;
            border-radius: 12px;
            border: 1px solid #e5e7eb;
        }

        .course h3 {
            margin-bottom: 12px;
            color: #1d4ed8;
        }

        .course p {
            line-height: 1.6;
            margin-bottom: 15px;
        }


        /* CONTACT */

        .contact {
            background: #eaf2ff;
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
            background: white;
            width: 260px;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.07);
        }

        .contact-box h3 {
            margin-bottom: 15px;
        }

        .contact-box p {
            margin-bottom: 20px;
            word-break: break-word;
        }


        /* SOCIAL MEDIA */

        .social {
            background: white;
            text-align: center;
        }

        .social a {
            display: inline-block;
            margin: 10px;
            padding: 14px 25px;
            background: #111827;
            color: white;
            text-decoration: none;
            border-radius: 8px;
        }

        .social a:hover {
            background: #2563eb;
        }


        /* FOOTER */

        footer {
            background: #111827;
            color: white;
            text-align: center;
            padding: 30px;
        }

        footer p {
            margin: 5px;
        }


        /* MOBILE */

        @media (max-width: 700px) {

            nav {
                flex-direction: column;
                gap: 15px;
            }

            nav div {
                text-align: center;
            }

            nav a {
                margin: 5px;
                display: inline-block;
            }

            .hero h1 {
                font-size: 42px;
            }

            .hero h3 {
                font-size: 22px;
            }

            .hero p {
                font-size: 17px;
            }

            section {
                padding: 60px 5%;
            }

            section h2 {
                font-size: 32px;
            }
        }

    </style>
</head>


<body>


<!-- NAVIGATION -->

<nav>

    <h2>Career Bridge</h2>

    <div>

        <a href="#home">Home</a>

        <a href="#about">About</a>

        <a href="#services">Services</a>

        <a href="#courses">Courses</a>

        <a href="#contact">Contact</a>

    </div>

</nav>



<!-- HOME -->

<section class="hero" id="home">

    <h1>Career Bridge</h1>

    <h3>Build Skills. Build Your Future.</h3>

    <p>
        Career Bridge helps students develop practical skills,
        create professional CVs and prepare for future career opportunities.
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

        <strong>to help students build skills today for the opportunities of tomorrow.</strong>
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

    <h2>Reach Me</h2>

    <p class="section-intro">
        Have a question or interested in our services?
        You can reach me through any of the options below.
    </p>


    <div class="contact-options">


        <!-- EMAIL -->

        <div class="contact-box">

            <h3>📧 Email</h3>

            <p>
                Send me an email for enquiries and business questions.
            </p>

            <a
                href="mailto:maxwellamenah11@gmail.com"
                class="button">
                Send Email
            </a>

        </div>



        <!-- WHATSAPP -->

        <div class="contact-box">

            <h3>💬 WhatsApp</h3>

            <p>
                Chat with me directly on WhatsApp.
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
        Follow me for career tips, learning opportunities
        and useful student content.
    </p>


    <a
        href="https://www.tiktok.com/@maxwell6573"
        target="_blank">
        🎵 TikTok
    </a>


    <a
        href="mailto:maxwellamenah11@gmail.com">
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

    <p><strong>Career Bridge</strong></p>

    <p>
        Building skills. Connecting opportunities.
    </p>

    <p>
        © 2026 Career Bridge. All rights reserved.
    </p>

</footer>


</body>
</html>
"""


if __name__ == "__main__":
    app.run(debug=True)
