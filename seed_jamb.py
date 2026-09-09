from datetime import datetime
import random
import math

from app import app, db, JAMBQuestion


# ============================================================
# CAREER BRIDGE — EXTREME JAMB-STYLE QUESTION BANK SEEDER
# ============================================================
#
# Original practice questions only.
# NOT official JAMB past questions.
#
# Target:
#   1,000 questions per subject
#
# Subjects:
#   13
#
# Total target:
#   13,000 questions
#
# ============================================================


TARGET_PER_SUBJECT = 1000
DIFFICULTY = "Extreme"
RANDOM_SEED = 20260908


SUBJECTS = [
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
    "Computer Science",
]


# ============================================================
# HELPERS
# ============================================================

def count_subject(subject):
    return JAMBQuestion.query.filter_by(
        subject=subject
    ).count()


def _unique_options(values):
    result = []

    for value in values:
        value = str(value)

        if value not in result:
            result.append(value)

    if len(result) != 4:
        raise ValueError(
            f"Expected 4 unique options, got {result}"
        )

    return result


def add_question(
    subject,
    question,
    options,
    answer_index,
    topic,
    subtopic,
    explanation
):

    if len(options) != 4:
        raise ValueError(
            "Each question must have exactly four options."
        )

    options = _unique_options(options)

    if not 0 <= answer_index < 4:
        raise ValueError(
            "answer_index must be between 0 and 3."
        )

    question = question.strip()

    if not question:
        raise ValueError(
            "Question cannot be empty."
        )

    banned_words = (
        "practice item",
        "sentence set",
        "extreme challenge",
        "question number"
    )

    if any(
        banned in question.lower()
        for banned in banned_words
    ):
        raise ValueError(
            f"Artificial wording detected: {question}"
        )

    existing = JAMBQuestion.query.filter_by(
        subject=subject,
        question=question
    ).first()

    if existing:
        return False

    correct = options[answer_index]

    shuffled = list(options)
    random.shuffle(shuffled)

    correct_letter = "ABCD"[
        shuffled.index(correct)
    ]

    db.session.add(
        JAMBQuestion(
            year=None,
            subject=subject,
            topic=topic,
            subtopic=subtopic,
            difficulty=DIFFICULTY,
            question=question,
            option_a=shuffled[0],
            option_b=shuffled[1],
            option_c=shuffled[2],
            option_d=shuffled[3],
            correct_answer=correct_letter,
            explanation=explanation,
            source=(
                "Career Bridge Original "
                "Extreme Practice Question"
            ),
            created_at=datetime.utcnow()
        )
    )

    return True


def cleanup_legacy_generated_questions():

    rows = JAMBQuestion.query.filter(
        (JAMBQuestion.question.ilike("%sentence set%")) |
        (JAMBQuestion.question.ilike("%practice item%")) |
        (JAMBQuestion.question.ilike("%extreme challenge%"))
    ).all()

    removed = 0

    for row in rows:
        db.session.delete(row)
        removed += 1

    if removed:
        db.session.commit()

        print(
            f"Removed {removed} legacy questions.",
            flush=True
        )

    return removed


# ============================================================
# EFFICIENT GENERATION LOOP
# ============================================================

def add_until(subject, target, generator):

    existing = count_subject(subject)

    needed = target - existing

    if needed <= 0:
        return

    created = 0
    attempts = 0
    skipped = 0

    max_attempts = max(
        10000,
        needed * 50
    )

    while created < needed:

        attempts += 1

        if attempts > max_attempts:

            raise RuntimeError(
                f"Could not generate enough questions "
                f"for {subject}. "
                f"Created {created}/{needed}."
            )

        try:

            result = generator()

            if result:
                created += 1

        except ValueError as exc:

            skipped += 1
            db.session.rollback()

            print(
                f"Skipping malformed {subject} question: {exc}",
                flush=True
            )

        except Exception as exc:

            skipped += 1
            db.session.rollback()

            print(
                f"Skipping failed {subject} question: {exc}",
                flush=True
            )

        if created > 0 and created % 100 == 0:

            db.session.commit()

            print(
                f"  {subject}: "
                f"{created}/{needed} generated",
                flush=True
            )

    db.session.commit()


# ============================================================
# 1. USE OF ENGLISH
# ============================================================

def english_generator():

    styles = [

        "grammar",
        "vocabulary",
        "concord",
        "idiom",
        "inference",
        "register",
        "sentence_completion",
        "word_class",
        "meaning",
        "punctuation"
    ]

    style = random.choice(styles)

    if style == "grammar":

        subjects = [
            ("Neither the director nor the accountants", "were"),
            ("The committee, together with its advisers", "has"),
            ("Each of the candidates", "was"),
            ("A number of students", "have"),
            ("The quality of the arguments", "is"),
            ("Neither the teachers nor the principal", "was"),
        ]

        phrase, correct = random.choice(subjects)

        options = [
            correct,
            "are" if correct == "is" else "is",
            "have" if correct == "has" else "has",
            "were" if correct == "was" else "was"
        ]

        return add_question(
            "Use of English",
            (
                f"Choose the option that correctly completes "
                f"the sentence: {phrase} ______ responsible "
                f"for the decision."
            ),
            options,
            0,
            "Grammar",
            "Subject-verb agreement",
            (
                "The verb must agree with the grammatical "
                "subject rather than with a nearby noun."
            )
        )

    if style == "concord":

        pairs = [
            ("Mathematics", "is"),
            ("The news", "was"),
            ("Politics", "is"),
            ("The furniture", "was"),
            ("The equipment", "has"),
            ("The information", "was"),
        ]

        noun, correct = random.choice(pairs)

        return add_question(
            "Use of English",
            (
                f"Which option correctly completes the sentence: "
                f"'{noun} ______ carefully examined before "
                f"the report was released'?"
            ),
            [
                correct,
                "are",
                "were",
                "have been"
            ],
            0,
            "Grammar",
            "Concord",
            (
                f"'{noun}' functions as a singular mass or "
                "uncountable expression in this context."
            )
        )

    if style == "vocabulary":

        data = [
            (
                "mitigate",
                "reduce the severity of something",
                "increase its severity",
                "conceal its existence",
                "predict its occurrence"
            ),
            (
                "ambiguous",
                "open to more than one interpretation",
                "completely false",
                "highly technical",
                "emotionally persuasive"
            ),
            (
                "pragmatic",
                "concerned with practical consequences",
                "based entirely on tradition",
                "opposed to evidence",
                "purely theoretical"
            ),
            (
                "inadvertent",
                "unintentional",
                "carefully planned",
                "publicly announced",
                "legally prohibited"
            ),
            (
                "scrupulous",
                "very careful and principled",
                "careless and impulsive",
                "secretive and dishonest",
                "physically exhausted"
            )
        ]

        word, correct, a, b, c = random.choice(data)

        return add_question(
            "Use of English",
            (
                f"In the sentence, 'The committee introduced "
                f"several measures to {word} the effect of the "
                f"policy,' the word '{word}' most nearly means:"
            ),
            [
                correct,
                a,
                b,
                c
            ],
            0,
            "Vocabulary",
            "Contextual meaning",
            (
                f"The word '{word}' means {correct.lower()}."
            )
        )

    if style == "idiom":

        data = [
            (
                "The minister refused to jump the gun",
                "act before the appropriate time",
                "withdraw from the contest",
                "change the law suddenly",
                "avoid public criticism"
            ),
            (
                "The researcher hit the nail on the head",
                "identified the exact issue",
                "damaged the experiment",
                "ended the investigation",
                "ignored the evidence"
            ),
            (
                "The witness let the cat out of the bag",
                "revealed a secret",
                "escaped from danger",
                "changed the subject",
                "rejected an accusation"
            ),
            (
                "The new policy was a blessing in disguise",
                "appeared harmful but produced an unexpected benefit",
                "was openly celebrated from the beginning",
                "was deliberately hidden",
                "was impossible to implement"
            )
        ]

        expression, correct, a, b, c = random.choice(data)

        return add_question(
            "Use of English",
            (
                f"What does the expression '{expression}' "
                "mean in context?"
            ),
            [
                correct,
                a,
                b,
                c
            ],
            0,
            "Lexis and Structure",
            "Idiomatic expressions",
            (
                "The correct option gives the contextual "
                "meaning of the idiomatic expression."
            )
        )

    if style == "word_class":

        data = [
            ("remarkably", "adverb"),
            ("careful", "adjective"),
            ("decision", "noun"),
            ("strengthen", "verb"),
            ("although", "conjunction"),
            ("beneath", "preposition"),
            ("wisdom", "noun"),
            ("rapidly", "adverb"),
        ]

        word, correct = random.choice(data)

        return add_question(
            "Use of English",
            (
                f"What is the grammatical function of "
                f"'{word}' in the sentence: "
                f"'The researcher worked {word} to complete "
                f"the analysis'?"
            ),
            [
                correct,
                "noun",
                "adjective",
                "preposition"
            ],
            0,
            "Grammar",
            "Word classes",
            (
                f"'{word}' is functioning as a {correct.lower()} "
                "in the stated construction."
            )
        )

    if style == "register":

        data = [
            (
                "The surgeon prepared the patient for the procedure.",
                "medical",
                "legal",
                "journalistic",
                "commercial"
            ),
            (
                "The plaintiff filed a claim before the court.",
                "legal",
                "medical",
                "agricultural",
                "musical"
            ),
            (
                "The company recorded a liability in its statement.",
                "accounting",
                "medical",
                "literary",
                "agricultural"
            )
        ]

        sentence, correct, a, b, c = random.choice(data)

        return add_question(
            "Use of English",
            (
                f"The sentence '{sentence}' is most strongly "
                f"associated with which register?"
            ),
            [
                correct,
                a,
                b,
                c
            ],
            0,
            "Lexis",
            "Register",
            (
                "The terminology and context determine the "
                "appropriate professional register."
            )
        )

    if style == "meaning":

        data = [
            (
                "The chairman's response was measured.",
                "careful and controlled",
                "extremely loud",
                "mathematically calculated",
                "completely irrelevant"
            ),
            (
                "The proposal was untenable.",
                "unable to be defended or maintained",
                "highly profitable",
                "widely celebrated",
                "legally compulsory"
            ),
            (
                "Her explanation was coherent.",
                "logical and consistent",
                "brief and incomplete",
                "emotionally aggressive",
                "intentionally deceptive"
            )
        ]

        sentence, correct, a, b, c = random.choice(data)

        return add_question(
            "Use of English",
            (
                f"In the sentence '{sentence}', the word "
                "in bold most nearly means:"
            ),
            [
                correct,
                a,
                b,
                c
            ],
            0,
            "Vocabulary",
            "Synonym in context",
            (
                "The correct option preserves the meaning "
                "of the word as used in context."
            )
        )

    if style == "punctuation":

        return add_question(
            "Use of English",
            (
                "Which sentence is punctuated correctly?"
            ),
            [
                "After the lecture, the students submitted their reports.",
                "After the lecture the students, submitted their reports.",
                "After, the lecture the students submitted their reports.",
                "After the lecture the students submitted, their reports."
            ],
            0,
            "Grammar",
            "Punctuation",
            (
                "A comma appropriately separates the introductory "
                "phrase from the main clause."
            )
        )

    if style == "sentence_completion":

        data = [
            (
                "Although the evidence appeared convincing, "
                "the investigator remained ______.",
                "skeptical",
                ["reckless", "indifferent", "careless"]
            ),
            (
                "The chairman's explanation was so ______ that "
                "even the opposing members accepted it.",
                "persuasive",
                ["ambiguous", "irrelevant", "fragmentary"]
            ),
            (
                "Because the instructions were ______, several "
                "candidates interpreted them differently.",
                "ambiguous",
                ["precise", "explicit", "unambiguous"]
            )
        ]

        sentence, correct, wrong = random.choice(data)

        return add_question(
            "Use of English",
            sentence,
            [correct] + wrong,
            0,
            "Lexis and Structure",
            "Sentence completion",
            (
                "The context establishes the relationship between "
                "the blank and the rest of the sentence."
            )
        )

    # inference

    passages = [
        (
            "The school installed computers in every classroom. "
            "Three months later, examination results remained "
            "unchanged, although students reported spending more "
            "time using digital resources.",
            "The introduction of computers alone did not necessarily "
            "produce an immediate improvement in examination results.",
            [
                "Every student failed to use the computers.",
                "The computers were removed after three months.",
                "Examination results always decline after technology is introduced."
            ]
        ),
        (
            "The farmer increased fertilizer application twice "
            "during the season. Crop yield rose initially but fell "
            "after the second application.",
            "More fertilizer did not necessarily continue to increase yield.",
            [
                "The farmer used no fertilizer at all.",
                "Fertilizer can never increase crop yield.",
                "The crop was harvested before fertilizer was applied."
            ]
        )
    ]

    passage, correct, wrong = random.choice(passages)

    return add_question(
        "Use of English",
        (
            "Read the passage and choose the conclusion that "
            "is best supported.\n\n"
            + passage
        ),
        [correct] + wrong,
        0,
        "Comprehension",
        "Inference",
        (
            "The conclusion must be supported by the information "
            "given rather than by an assumption outside the passage."
        )
    )


# ============================================================
# 2. MATHEMATICS
# ============================================================

def mathematics_generator():

    kind = random.choice([
        "quadratic",
        "simultaneous",
        "sequence",
        "probability",
        "percentage",
        "indices",
        "logarithm",
        "geometry",
        "variation",
        "modular"
    ])

    if kind == "quadratic":

        r1 = random.randint(-12, 12)
        r2 = random.randint(-12, 12)

        if r1 == r2:
            r2 += 1

        b = -(r1 + r2)
        c = r1 * r2

        return add_question(
            "Mathematics",
            (
                f"If x² + ({b})x + ({c}) = 0, what is the "
                "product of the roots?"
            ),
            [
                str(c),
                str(-c),
                str(r1 + r2),
                str(-(r1 + r2))
            ],
            0,
            "Algebra",
            "Quadratic equations",
            (
                "For x² + bx + c = 0, the product of the "
                "roots is c."
            )
        )

    if kind == "simultaneous":

        x = random.randint(3, 20)
        y = random.randint(2, 15)

        a = random.randint(2, 7)
        b = random.randint(2, 7)

        c = a * x + b * y

        d = random.randint(2, 7)
        e = random.randint(2, 7)

        while d * x + e * y == c:
            e = random.randint(2, 7)

        f = d * x + e * y

        return add_question(
            "Mathematics",
            (
                f"Given that {a}x + {b}y = {c} and "
                f"{d}x + {e}y = {f}, determine x."
            ),
            [
                str(x),
                str(y),
                str(x + y),
                str(abs(x - y))
            ],
            0,
            "Algebra",
            "Simultaneous equations",
            (
                "The two linear equations can be solved "
                "simultaneously by elimination or substitution."
            )
        )

    if kind == "sequence":

        first = random.randint(2, 30)
        difference = random.randint(2, 15)
        n = random.randint(8, 25)

        value = first + (n - 1) * difference

        return add_question(
            "Mathematics",
            (
                f"An arithmetic progression has first term "
                f"{first} and common difference {difference}. "
                f"What is its {n}th term?"
            ),
            [
                str(value),
                str(value + difference),
                str(value - difference),
                str(first + n * difference)
            ],
            0,
            "Sequences",
            "Arithmetic progression",
            (
                "Use the formula aₙ = a + (n − 1)d."
            )
        )

    if kind == "probability":

        red = random.randint(3, 12)
        blue = random.randint(3, 12)
        green = random.randint(2, 10)

        total = red + blue + green

        probability = red / total

        rounded = round(probability, 3)

        return add_question(
            "Mathematics",
            (
                f"A bag contains {red} red, {blue} blue and "
                f"{green} green balls. One ball is selected at "
                "random. What is the probability that it is red?"
            ),
            [
                f"{red}/{total}",
                f"{blue}/{total}",
                f"{green}/{total}",
                f"{total}/{red}"
            ],
            0,
            "Probability",
            "Simple probability",
            (
                "Probability equals the number of favourable "
                "outcomes divided by the total number of outcomes."
            )
        )

    if kind == "percentage":

        original = random.randint(200, 2000)
        increase = random.randint(10, 40)
        decrease = random.randint(5, 30)

        final = original * (1 + increase / 100)
        final *= (1 - decrease / 100)

        correct = round(final, 2)

        return add_question(
            "Mathematics",
            (
                f"A quantity of {original} is increased by "
                f"{increase}% and then decreased by {decrease}%. "
                f"What is the resulting value?"
            ),
            [
                str(correct),
                str(round(original * (1 + (increase - decrease) / 100), 2)),
                str(round(original * (1 + increase / 100), 2)),
                str(round(original * (1 - decrease / 100), 2))
            ],
            0,
            "Number",
            "Percentage change",
            (
                "Successive percentage changes are applied "
                "multiplicatively, not simply added or subtracted."
            )
        )

    if kind == "indices":

        a = random.randint(2, 6)
        m = random.randint(2, 5)
        n = random.randint(2, 5)

        exponent = m + n
        correct = a ** exponent

        return add_question(
            "Mathematics",
            (
                f"Simplify ({a}^{m})({a}^{n})."
            ),
            [
                str(correct),
                str(a ** (m * n)),
                str(a ** (m - n)),
                str((a ** m) + (a ** n))
            ],
            0,
            "Indices",
            "Laws of indices",
            (
                "When powers with the same base are multiplied, "
                "their exponents are added."
            )
        )

    if kind == "logarithm":

        base = random.choice([2, 3, 5, 10])
        exponent = random.randint(2, 6)

        value = base ** exponent

        return add_question(
            "Mathematics",
            (
                f"Evaluate log base {base} of {value}."
            ),
            [
                str(exponent),
                str(base),
                str(value),
                str(exponent * base)
            ],
            0,
            "Logarithms",
            "Logarithmic laws",
            (
                f"{base}^{exponent} = {value}, therefore "
                f"log base {base} of {value} = {exponent}."
            )
        )

    if kind == "geometry":

        length = random.randint(5, 30)
        width = random.randint(4, 20)

        area = length * width

        return add_question(
            "Mathematics",
            (
                f"A rectangular field has length {length} m "
                f"and width {width} m. A path of negligible width "
                "is ignored. What is the area of the field?"
            ),
            [
                f"{area} m²",
                f"{2 * (length + width)} m²",
                f"{length + width} m²",
                f"{area * 2} m²"
            ],
            0,
            "Geometry",
            "Area",
            (
                "The area of a rectangle is length multiplied "
                "by width."
            )
        )

    if kind == "variation":

        k = random.randint(2, 15)
        x1 = random.randint(2, 10)
        y1 = k * x1 ** 2

        x2 = random.randint(11, 20)
        y2 = k * x2 ** 2

        return add_question(
            "Mathematics",
            (
                f"y varies directly as x². If y = {y1} when "
                f"x = {x1}, what is y when x = {x2}?"
            ),
            [
                str(y2),
                str(k * x2),
                str(y1 + x2),
                str(k * x1 * x2)
            ],
            0,
            "Variation",
            "Direct variation",
            (
                "Since y ∝ x², y = kx². Find k from the first "
                "pair and substitute the new x."
            )
        )

    # modular arithmetic

    modulus = random.randint(5, 15)
    a = random.randint(20, 100)
    b = random.randint(10, 50)

    correct = (a + b) % modulus

    return add_question(
        "Mathematics",
        (
            f"What is the remainder when {a + b} is divided "
            f"by {modulus}?"
        ),
        [
            str(correct),
            str((a - b) % modulus),
            str(a % modulus),
            str(b % modulus)
        ],
        0,
        "Number",
        "Remainders",
        (
            "Divide the number by the modulus and identify "
            "the non-negative remainder."
        )
    )


# ============================================================
# 3. PHYSICS
# ============================================================

def physics_generator():

    kind = random.choice([
        "motion",
        "force",
        "energy",
        "momentum",
        "electricity",
        "waves",
        "pressure",
        "density",
        "heat",
        "power"
    ])

    if kind == "motion":

        u = random.randint(2, 15)
        acceleration = random.randint(1, 8)
        time = random.randint(2, 10)

        v = u + acceleration * time

        return add_question(
            "Physics",
            (
                f"A body moves with initial velocity {u} m/s "
                f"and accelerates uniformly at {acceleration} m/s² "
                f"for {time} s. What is its final velocity?"
            ),
            [
                f"{v} m/s",
                f"{u + acceleration} m/s",
                f"{u * time} m/s",
                f"{v + acceleration} m/s"
            ],
            0,
            "Mechanics",
            "Uniform acceleration",
            (
                "Use v = u + at."
            )
        )

    if kind == "force":

        mass = random.randint(2, 20)
        acceleration = random.randint(2, 10)

        force = mass * acceleration

        return add_question(
            "Physics",
            (
                f"A body of mass {mass} kg accelerates at "
                f"{acceleration} m/s². What net force acts on it?"
            ),
            [
                f"{force} N",
                f"{mass + acceleration} N",
                f"{force / mass:g} N",
                f"{mass / acceleration:g} N"
            ],
            0,
            "Mechanics",
            "Newton's second law",
            (
                "Newton's second law gives F = ma."
            )
        )

    if kind == "energy":

        mass = random.randint(2, 20)
        height = random.randint(3, 30)
        g = 10

        energy = mass * g * height

        return add_question(
            "Physics",
            (
                f"Taking g = 10 m/s², calculate the gravitational "
                f"potential energy of a {mass} kg object raised "
                f"to a height of {height} m."
            ),
            [
                f"{energy} J",
                f"{mass * height} J",
                f"{mass * g} J",
                f"{energy / 10:g} J"
            ],
            0,
            "Energy",
            "Gravitational potential energy",
            (
                "GPE = mgh."
            )
        )

    if kind == "momentum":

        mass = random.randint(2, 15)
        velocity = random.randint(3, 20)

        momentum = mass * velocity

        return add_question(
            "Physics",
            (
                f"A body of mass {mass} kg moves at {velocity} m/s. "
                "What is its momentum?"
            ),
            [
                f"{momentum} kg m/s",
                f"{mass + velocity} kg m/s",
                f"{velocity / mass:g} kg m/s",
                f"{mass * velocity * 2} kg m/s"
            ],
            0,
            "Mechanics",
            "Momentum",
            (
                "Momentum is mass multiplied by velocity."
            )
        )

    if kind == "electricity":

        voltage = random.randint(6, 24)
        resistance = random.randint(2, 12)

        current = voltage / resistance

        if current.is_integer():
            current_text = str(int(current))
        else:
            current_text = f"{current:.2f}"

        return add_question(
            "Physics",
            (
                f"A resistor of {resistance} Ω is connected "
                f"to a {voltage} V source. What current flows?"
            ),
            [
                f"{current_text} A",
                f"{voltage * resistance} A",
                f"{resistance / voltage:.2f} A",
                f"{voltage + resistance} A"
            ],
            0,
            "Electricity",
            "Ohm's law",
            (
                "Ohm's law states that V = IR, therefore "
                "I = V/R."
            )
        )

    if kind == "waves":

        frequency = random.randint(2, 20)
        wavelength = random.randint(2, 15)

        speed = frequency * wavelength

        return add_question(
            "Physics",
            (
                f"A wave has frequency {frequency} Hz and "
                f"wavelength {wavelength} m. What is its speed?"
            ),
            [
                f"{speed} m/s",
                f"{frequency + wavelength} m/s",
                f"{frequency / wavelength:g} m/s",
                f"{wavelength / frequency:g} m/s"
            ],
            0,
            "Waves",
            "Wave equation",
            (
                "Wave speed is v = fλ."
            )
        )

    if kind == "pressure":

        force = random.randint(20, 200)
        area = random.randint(2, 20)

        pressure = force / area

        return add_question(
            "Physics",
            (
                f"A force of {force} N acts uniformly on an "
                f"area of {area} m². Calculate the pressure."
            ),
            [
                f"{pressure:g} Pa",
                f"{force * area:g} Pa",
                f"{area / force:g} Pa",
                f"{force + area:g} Pa"
            ],
            0,
            "Mechanics",
            "Pressure",
            (
                "Pressure is force divided by area."
            )
        )

    if kind == "density":

        volume = random.randint(2, 20)
        density = random.randint(500, 5000)

        mass = density * volume

        return add_question(
            "Physics",
            (
                f"A material has density {density} kg/m³ and "
                f"volume {volume} m³. What is its mass?"
            ),
            [
                f"{mass} kg",
                f"{density + volume} kg",
                f"{density / volume:g} kg",
                f"{mass / 2:g} kg"
            ],
            0,
            "Properties of Matter",
            "Density",
            (
                "Density = mass/volume, therefore mass = density × volume."
            )
        )

    if kind == "heat":

        mass = random.randint(1, 10)
        specific_heat = random.randint(300, 1000)
        temperature_change = random.randint(5, 40)

        heat = mass * specific_heat * temperature_change

        return add_question(
            "Physics",
            (
                f"A {mass} kg substance has specific heat capacity "
                f"{specific_heat} J/kgK. How much heat is required "
                f"to raise its temperature by {temperature_change} K?"
            ),
            [
                f"{heat} J",
                f"{mass * specific_heat} J",
                f"{specific_heat * temperature_change} J",
                f"{mass * temperature_change} J"
            ],
            0,
            "Heat",
            "Specific heat capacity",
            (
                "Use Q = mcΔT."
            )
        )

    power = random.randint(100, 2000)
    time = random.randint(2, 20)

    energy = power * time

    return add_question(
        "Physics",
        (
            f"An electrical appliance operates at {power} W "
            f"for {time} seconds. How much energy does it use?"
        ),
        [
            f"{energy} J",
            f"{power + time} J",
            f"{power / time:g} J",
            f"{energy / 2:g} J"
        ],
        0,
        "Energy",
        "Power",
        (
            "Energy = power × time."
        )
    )


# ============================================================
# 4. CHEMISTRY
# ============================================================

def chemistry_generator():

    kind = random.choice([
        "mole",
        "atomic",
        "periodic",
        "acid",
        "gas",
        "redox",
        "organic",
        "equilibrium",
        "electrolysis",
        "bonding"
    ])

    if kind == "mole":

        mass = random.randint(10, 100)
        molar_mass = random.choice([
            18,
            20,
            40,
            44,
            58.5,
            98
        ])

        moles = mass / molar_mass

        return add_question(
            "Chemistry",
            (
                f"A sample has a mass of {mass} g and molar mass "
                f"{molar_mass} g/mol. Approximately how many moles "
                "does it contain?"
            ),
            [
                f"{moles:.3f} mol",
                f"{mass * molar_mass:.1f} mol",
                f"{molar_mass / mass:.3f} mol",
                f"{mass + molar_mass:.1f} mol"
            ],
            0,
            "Stoichiometry",
            "Mole concept",
            (
                "Number of moles = mass / molar mass."
            )
        )

    if kind == "atomic":

        atomic_numbers = [
            (6, "carbon"),
            (8, "oxygen"),
            (11, "sodium"),
            (17, "chlorine"),
            (20, "calcium"),
            (13, "aluminium")
        ]

        number, element = random.choice(
            atomic_numbers
        )

        return add_question(
            "Chemistry",
            (
                f"An atom of {element.capitalize()} has atomic "
                f"number {number}. How many protons does a neutral "
                "atom of the element contain?"
            ),
            [
                str(number),
                str(number * 2),
                str(number - 1),
                str(number + 1)
            ],
            0,
            "Atomic Structure",
            "Atomic number",
            (
                "The atomic number equals the number of protons "
                "in the nucleus."
            )
        )

    if kind == "periodic":

        data = [
            (
                "Which property generally increases across a period?",
                "Effective nuclear attraction generally increases.",
                "Atomic radius always increases.",
                "Metallic character always increases.",
                "The number of occupied shells increases."
            ),
            (
                "Why do elements in the same group often show similar chemical behaviour?",
                "They have similar numbers of valence electrons.",
                "They have identical atomic masses.",
                "They contain the same number of shells.",
                "They all have the same atomic number."
            )
        ]

        question, correct, a, b, c = random.choice(data)

        return add_question(
            "Chemistry",
            question,
            [
                correct,
                a,
                b,
                c
            ],
            0,
            "Periodic Table",
            "Periodic trends",
            (
                "Periodic behaviour is strongly influenced by "
                "electron arrangement and effective nuclear charge."
            )
        )

    if kind == "acid":

        concentration = random.choice([
            0.001,
            0.01,
            0.1
        ])

        pH = round(-math.log10(concentration), 2)

        return add_question(
            "Chemistry",
            (
                f"Assuming complete ionisation, what is the pH "
                f"of a {concentration} mol/dm³ monoprotic strong acid?"
            ),
            [
                str(pH),
                str(round(14 - pH, 2)),
                str(round(pH + 1, 2)),
                str(round(pH / 2, 2))
            ],
            0,
            "Acids and Bases",
            "pH",
            (
                "For a strong monoprotic acid, [H⁺] equals the "
                "acid concentration, so pH = −log[H⁺]."
            )
        )

    if kind == "gas":

        pressure1 = random.randint(1, 5)
        volume1 = random.randint(2, 10)
        pressure2 = random.randint(1, 5)

        volume2 = (
            pressure1 * volume1 / pressure2
        )

        return add_question(
            "Chemistry",
            (
                f"A fixed mass of gas occupies {volume1} dm³ at "
                f"{pressure1} atm. If temperature is constant and "
                f"pressure changes to {pressure2} atm, what volume "
                "will the gas occupy?"
            ),
            [
                f"{volume2:g} dm³",
                f"{pressure1 * pressure2 * volume1:g} dm³",
                f"{volume1 * pressure2:g} dm³",
                f"{volume1 / pressure2:g} dm³"
            ],
            0,
            "Gases",
            "Boyle's law",
            (
                "At constant temperature, pressure and volume "
                "are inversely proportional: P₁V₁ = P₂V₂."
            )
        )

    if kind == "redox":

        return add_question(
            "Chemistry",
            (
                "In a redox reaction, an increase in oxidation "
                "number of an element represents:"
            ),
            [
                "oxidation",
                "reduction",
                "neutralisation",
                "precipitation"
            ],
            0,
            "Redox",
            "Oxidation numbers",
            (
                "Oxidation corresponds to an increase in oxidation "
                "number, while reduction corresponds to a decrease."
            )
        )

    if kind == "organic":

        data = [
            (
                "Which functional group characterises alcohols?",
                "hydroxyl",
                "carboxyl",
                "carbonyl",
                "amino"
            ),
            (
                "What is the general formula of an alkane?",
                "CₙH₂ₙ₊₂",
                "CₙH₂ₙ",
                "CₙH₂ₙ₋₂",
                "CₙHₙ"
            ),
            (
                "Which process converts an alkene into a saturated alkane?",
                "hydrogenation",
                "esterification",
                "oxidation",
                "hydrolysis"
            )
        ]

        question, correct, a, b, c = random.choice(data)

        return add_question(
            "Chemistry",
            question,
            [
                correct,
                a,
                b,
                c
            ],
            0,
            "Organic Chemistry",
            "Functional groups and reactions",
            (
                "The correct answer follows from the structural "
                "properties of the organic compound."
            )
        )

    if kind == "equilibrium":

        return add_question(
            "Chemistry",
            (
                "For a reversible exothermic reaction at equilibrium, "
                "what is the expected effect of increasing temperature?"
            ),
            [
                "The equilibrium shifts toward the endothermic direction.",
                "The equilibrium always shifts toward products.",
                "The equilibrium constant must become zero.",
                "The concentration of every species becomes equal."
            ],
            0,
            "Chemical Equilibrium",
            "Le Chatelier's principle",
            (
                "Increasing temperature favours the direction that "
                "absorbs heat, which is the endothermic direction."
            )
        )

    if kind == "electrolysis":

        return add_question(
            "Chemistry",
            (
                "During electrolysis, reduction occurs at which electrode?"
            ),
            [
                "cathode",
                "anode",
                "salt bridge",
                "electrolyte surface"
            ],
            0,
            "Electrochemistry",
            "Electrolysis",
            (
                "Reduction occurs at the cathode. A useful memory "
                "aid is Red Cat: reduction at cathode."
            )
        )

    return add_question(
        "Chemistry",
        (
            "Which type of bonding involves attraction between "
            "positive metal ions and delocalised electrons?"
        ),
        [
            "metallic bonding",
            "hydrogen bonding",
            "covalent bonding",
            "coordinate bonding"
        ],
        0,
        "Chemical Bonding",
        "Metallic bonding",
        (
            "Metallic bonding involves a lattice of positive ions "
            "surrounded by delocalised electrons."
        )
    )


# ============================================================
# 5. BIOLOGY
# ============================================================

def biology_generator():

    kind = random.choice([
        "cell",
        "genetics",
        "ecology",
        "physiology",
        "evolution",
        "nutrition",
        "reproduction",
        "classification",
        "transport",
        "homeostasis"
    ])

    if kind == "cell":

        return add_question(
            "Biology",
            (
                "A cell contains a structure that selectively "
                "controls movement of substances into and out "
                "of the cell. Which structure performs this role?"
            ),
            [
                "cell membrane",
                "cell wall",
                "nucleolus",
                "ribosome"
            ],
            0,
            "Cell Biology",
            "Cell membrane",
            (
                "The cell membrane is selectively permeable and "
                "regulates movement of substances."
            )
        )

    if kind == "genetics":

        return add_question(
            "Biology",
            (
                "Two heterozygous parents with genotype Aa are "
                "crossed. Assuming complete dominance, what is "
                "the probability of an offspring being homozygous recessive?"
            ),
            [
                "25%",
                "50%",
                "75%",
                "100%"
            ],
            0,
            "Genetics",
            "Monohybrid inheritance",
            (
                "Aa × Aa gives AA, Aa, Aa and aa. Therefore "
                "one out of four offspring is expected to be aa."
            )
        )

    if kind == "ecology":

        return add_question(
            "Biology",
            (
                "If a population increases rapidly beyond the "
                "carrying capacity of its environment, which outcome "
                "is most likely in the longer term?"
            ),
            [
                "Resource limitation will increase mortality or reduce reproduction.",
                "Resources will become unlimited.",
                "Competition will disappear.",
                "Predators will necessarily become extinct."
            ],
            0,
            "Ecology",
            "Population dynamics",
            (
                "Carrying capacity reflects environmental limitations "
                "such as food, space and other resources."
            )
        )

    if kind == "physiology":

        return add_question(
            "Biology",
            (
                "Why does an increase in carbon dioxide concentration "
                "in the blood normally stimulate faster breathing?"
            ),
            [
                "It contributes to increased acidity detected by regulatory mechanisms.",
                "It directly destroys all red blood cells.",
                "It causes the lungs to stop exchanging gases.",
                "It permanently closes the alveoli."
            ],
            0,
            "Physiology",
            "Respiration regulation",
            (
                "Elevated CO₂ contributes to increased hydrogen ion "
                "concentration, triggering respiratory regulation."
            )
        )

    if kind == "evolution":

        return add_question(
            "Biology",
            (
                "A population becomes separated geographically and "
                "the two groups accumulate genetic differences over "
                "many generations. Which process may eventually result?"
            ),
            [
                "speciation",
                "photosynthesis",
                "transpiration",
                "binary fission"
            ],
            0,
            "Evolution",
            "Speciation",
            (
                "Long-term reproductive isolation and genetic divergence "
                "can lead to formation of distinct species."
            )
        )

    if kind == "nutrition":

        nutrients = [
            (
                "vitamin C",
                "scurvy",
                "rickets",
                "night blindness",
                "goitre"
            ),
            (
                "vitamin D",
                "rickets",
                "scurvy",
                "beriberi",
                "anaemia"
            ),
            (
                "iron",
                "anaemia",
                "scurvy",
                "rickets",
                "diabetes"
            )
        ]

        nutrient, correct, a, b, c = random.choice(
            nutrients
        )

        return add_question(
            "Biology",
            (
                f"A prolonged deficiency of {nutrient} is most "
                f"strongly associated with which condition?"
            ),
            [
                correct,
                a,
                b,
                c
            ],
            0,
            "Nutrition",
            "Deficiency diseases",
            (
                "The correct condition is associated with deficiency "
                f"of {nutrient}."
            )
        )

    if kind == "reproduction":

        return add_question(
            "Biology",
            (
                "Which event during meiosis contributes directly "
                "to genetic variation by exchanging DNA between "
                "homologous chromosomes?"
            ),
            [
                "crossing over",
                "binary fission",
                "cytokinesis",
                "DNA translation"
            ],
            0,
            "Reproduction",
            "Meiosis",
            (
                "Crossing over exchanges genetic material between "
                "homologous chromosomes."
            )
        )

    if kind == "classification":

        return add_question(
            "Biology",
            (
                "Two organisms are classified in the same genus but "
                "different species. What does this indicate?"
            ),
            [
                "They share a relatively close evolutionary relationship.",
                "They must have identical DNA.",
                "They must occupy exactly the same habitat.",
                "They must have identical feeding mechanisms."
            ],
            0,
            "Classification",
            "Taxonomy",
            (
                "Members of the same genus share more recent common "
                "ancestry than organisms placed in different genera."
            )
        )

    if kind == "transport":

        return add_question(
            "Biology",
            (
                "Why is the wall of a typical capillary extremely thin?"
            ),
            [
                "To reduce the diffusion distance for exchange.",
                "To prevent all substances from crossing.",
                "To increase blood viscosity.",
                "To stop oxygen from entering tissues."
            ],
            0,
            "Transport",
            "Circulatory system",
            (
                "A thin capillary wall provides a short diffusion "
                "distance for gases, nutrients and waste products."
            )
        )

    return add_question(
        "Biology",
        (
            "Which statement best explains negative feedback in "
            "homeostasis?"
        ),
        [
            "A deviation from a set point triggers responses that tend to oppose the deviation.",
            "Every deviation is amplified indefinitely.",
            "The body stops responding to environmental changes.",
            "All physiological variables remain absolutely constant."
        ],
        0,
        "Homeostasis",
        "Negative feedback",
        (
            "Negative feedback reduces the original disturbance "
            "and helps maintain internal conditions within suitable limits."
        )
    )


# ============================================================
# 6. ECONOMICS
# ============================================================

def economics_generator():

    kind = random.choice([
        "elasticity",
        "opportunity",
        "inflation",
        "market",
        "production",
        "unemployment",
        "national_income",
        "taxation",
        "money",
        "development"
    ])

    if kind == "elasticity":

        percentage_change_quantity = random.choice([
            5,
            10,
            15,
            20,
            25
        ])

        percentage_change_price = random.choice([
            5,
            10,
            20,
            25
        ])

        elasticity = (
            percentage_change_quantity /
            percentage_change_price
        )

        return add_question(
            "Economics",
            (
                f"Demand for a product falls by "
                f"{percentage_change_quantity}% when its price "
                f"rises by {percentage_change_price}%. What is the "
                "absolute value of the price elasticity of demand?"
            ),
            [
                f"{elasticity:g}",
                f"{percentage_change_quantity + percentage_change_price:g}",
                f"{percentage_change_price / percentage_change_quantity:g}",
                f"{elasticity + 1:g}"
            ],
            0,
            "Demand",
            "Price elasticity",
            (
                "PED = percentage change in quantity demanded "
                "divided by percentage change in price."
            )
        )

    if kind == "opportunity":

        choices = [
            ("₦80,000", "₦80,000"),
            ("₦120,000", "₦120,000"),
            ("₦150,000", "₦150,000"),
            ("₦200,000", "₦200,000")
        ]

        best, cost = random.choice(choices)

        return add_question(
            "Economics",
            (
                f"A student can spend savings on a course costing "
                f"{cost} or on a business opportunity with a higher "
                "expected return. If the student chooses the course, "
                "what concept describes the value of the best "
                "alternative forgone?"
            ),
            [
                "opportunity cost",
                "fixed cost",
                "sunk cost",
                "average cost"
            ],
            0,
            "Basic Economic Concepts",
            "Opportunity cost",
            (
                "Opportunity cost is the value of the best "
                "alternative forgone."
            )
        )

    if kind == "inflation":

        return add_question(
            "Economics",
            (
                "If nominal income rises by 8% while the general "
                "price level rises by 12%, what is most likely true "
                "about real purchasing power?"
            ),
            [
                "It falls, assuming other factors remain unchanged.",
                "It must rise by exactly 20%.",
                "It remains unchanged.",
                "It doubles automatically."
            ],
            0,
            "Macroeconomics",
            "Inflation",
            (
                "When prices rise faster than nominal income, "
                "real purchasing power generally decreases."
            )
        )

    if kind == "market":

        return add_question(
            "Economics",
            (
                "A firm in a perfectly competitive market faces a "
                "horizontal demand curve at the market price. Why?"
            ),
            [
                "The individual firm is a price taker.",
                "The firm controls the entire market.",
                "There are no buyers.",
                "The government fixes every firm's output."
            ],
            0,
            "Market Structure",
            "Perfect competition",
            (
                "A competitive firm is too small relative to the "
                "market to influence the prevailing price."
            )
        )

    if kind == "production":

        return add_question(
            "Economics",
            (
                "If marginal product begins to fall while total "
                "product is still increasing, which statement is correct?"
            ),
            [
                "The total product is increasing at a decreasing rate.",
                "Total product must immediately become zero.",
                "Marginal product must be negative.",
                "Average product must immediately become zero."
            ],
            0,
            "Production",
            "Marginal product",
            (
                "A falling but positive marginal product means "
                "additional output is still being produced, but "
                "at a decreasing rate."
            )
        )

    if kind == "unemployment":

        return add_question(
            "Economics",
            (
                "A worker loses employment because the skills required "
                "by available jobs have changed significantly. This is "
                "best classified as:"
            ),
            [
                "structural unemployment",
                "frictional unemployment",
                "seasonal unemployment",
                "voluntary unemployment"
            ],
            0,
            "Labour Market",
            "Unemployment",
            (
                "Structural unemployment arises from a mismatch "
                "between workers' skills and available jobs."
            )
        )

    if kind == "national_income":

        return add_question(
            "Economics",
            (
                "Why can GDP per capita rise without every household "
                "experiencing an improvement in living standards?"
            ),
            [
                "Income distribution may be unequal.",
                "GDP never measures production.",
                "Population has no relationship with GDP per capita.",
                "All households always receive identical income."
            ],
            0,
            "National Income",
            "GDP per capita",
            (
                "GDP per capita is an average and does not show "
                "how income is distributed among households."
            )
        )

    if kind == "taxation":

        return add_question(
            "Economics",
            (
                "A tax whose rate rises as a taxpayer's income rises "
                "is described as:"
            ),
            [
                "progressive",
                "regressive",
                "proportional",
                "indirect"
            ],
            0,
            "Public Finance",
            "Taxation",
            (
                "A progressive tax takes an increasing proportion "
                "of income as income rises."
            )
        )

    if kind == "money":

        return add_question(
            "Economics",
            (
                "Which function of money is demonstrated when a "
                "shopkeeper quotes the price of a phone as ₦250,000?"
            ),
            [
                "unit of account",
                "medium of exchange",
                "store of value",
                "standard of deferred payment"
            ],
            0,
            "Money",
            "Functions of money",
            (
                "Using money to express prices provides a common "
                "unit for measuring value."
            )
        )

    return add_question(
        "Economics",
        (
            "Which combination is most likely to support long-term "
            "economic development?"
        ),
        [
            "investment in human capital, infrastructure and institutions",
            "persistent destruction of productive capacity",
            "reduction in education and health investment",
            "elimination of all technological innovation"
        ],
        0,
        "Economic Development",
        "Development policy",
        (
            "Human capital, infrastructure and effective institutions "
            "can increase productive capacity and support development."
        )
    )


# ============================================================
# 7. GOVERNMENT
# ============================================================

def government_generator():

    kind = random.choice([
        "constitution",
        "separation",
        "federalism",
        "democracy",
        "pressure",
        "election",
        "judiciary",
        "legislature",
        "citizenship",
        "international"
    ])

    if kind == "constitution":

        return add_question(
            "Government",
            (
                "What is the primary purpose of a constitution "
                "in a modern state?"
            ),
            [
                "to establish the framework and limits of government",
                "to eliminate all political disagreement",
                "to guarantee that every citizen holds public office",
                "to prevent citizens from participating in politics"
            ],
            0,
            "Constitution",
            "Functions of constitution",
            (
                "A constitution establishes governmental structures, "
                "powers, responsibilities and limits."
            )
        )

    if kind == "separation":

        return add_question(
            "Government",
            (
                "The separation of powers is intended primarily "
                "to prevent:"
            ),
            [
                "concentration and abuse of governmental power",
                "the existence of political parties",
                "all forms of public debate",
                "citizens from voting"
            ],
            0,
            "Political Institutions",
            "Separation of powers",
            (
                "Dividing governmental powers creates checks that "
                "can limit abuse."
            )
        )

    if kind == "federalism":

        return add_question(
            "Government",
            (
                "Which feature most clearly distinguishes a federal "
                "system from a unitary system?"
            ),
            [
                "constitutional division of powers between levels of government",
                "absence of any constitution",
                "complete abolition of local government",
                "government by military decree"
            ],
            0,
            "Political Systems",
            "Federalism",
            (
                "Federalism constitutionally distributes powers between "
                "the central and constituent governments."
            )
        )

    if kind == "democracy":

        return add_question(
            "Government",
            (
                "Why is an independent electoral process important "
                "to representative democracy?"
            ),
            [
                "It increases the credibility of citizens' choice of representatives.",
                "It guarantees that every candidate wins.",
                "It eliminates the need for political parties.",
                "It prevents citizens from changing governments."
            ],
            0,
            "Democracy",
            "Elections",
            (
                "Credible elections help translate citizens' preferences "
                "into legitimate political representation."
            )
        )

    if kind == "pressure":

        return add_question(
            "Government",
            (
                "A professional association repeatedly communicates "
                "policy proposals to lawmakers in an attempt to "
                "influence legislation. It is acting primarily as a:"
            ),
            [
                "pressure group",
                "judiciary",
                "civil service ministry",
                "political court"
            ],
            0,
            "Political Groups",
            "Pressure groups",
            (
                "Pressure groups seek to influence public policy "
                "without necessarily seeking to form the government."
            )
        )

    if kind == "election":

        return add_question(
            "Government",
            (
                "Which electoral principle means that each eligible "
                "voter's vote should have substantially equal weight?"
            ),
            [
                "equality of voting power",
                "hereditary succession",
                "collective responsibility",
                "judicial review"
            ],
            0,
            "Elections",
            "Electoral principles",
            (
                "Equal voting power is fundamental to representative "
                "electoral systems."
            )
        )

    if kind == "judiciary":

        return add_question(
            "Government",
            (
                "Judicial review allows a court to examine whether "
                "a governmental action or law is consistent with:"
            ),
            [
                "the constitution or applicable law",
                "the personal preference of a judge",
                "the wealth of the government",
                "the number of political parties"
            ],
            0,
            "Judiciary",
            "Judicial review",
            (
                "Judicial review concerns the legality or constitutionality "
                "of governmental action."
            )
        )

    if kind == "legislature":

        return add_question(
            "Government",
            (
                "The primary legislative function of a parliament is to:"
            ),
            [
                "make and amend laws",
                "interpret every law in court",
                "command the armed forces independently",
                "conduct private commercial transactions"
            ],
            0,
            "Legislature",
            "Functions of legislature",
            (
                "Legislatures are principally responsible for making laws."
            )
        )

    if kind == "citizenship":

        return add_question(
            "Government",
            (
                "Which situation best illustrates civic responsibility?"
            ),
            [
                "obeying lawful rules while participating responsibly in public affairs",
                "destroying public property during disagreements",
                "refusing every lawful obligation",
                "preventing others from expressing lawful opinions"
            ],
            0,
            "Citizenship",
            "Civic responsibility",
            (
                "Responsible citizenship involves lawful participation "
                "and respect for public institutions and other citizens."
            )
        )

    return add_question(
        "Government",
        (
            "Why do states participate in international organisations?"
        ),
        [
            "to cooperate on shared political, economic and security issues",
            "to surrender every aspect of national sovereignty automatically",
            "to eliminate all domestic institutions",
            "to prevent all international communication"
        ],
        0,
        "International Relations",
        "International organisations",
        (
            "States cooperate internationally because many issues "
            "cross national boundaries."
        )
    )


# ============================================================
# 8. LITERATURE
# ============================================================

def literature_generator():

    kind = random.choice([
        "plot",
        "character",
        "theme",
        "irony",
        "imagery",
        "symbolism",
        "dramatic",
        "poetry",
        "narrative",
        "tone"
    ])

    if kind == "plot":

        return add_question(
            "Literature",
            (
                "A protagonist makes a decision that creates a chain "
                "of consequences eventually leading to the climax. "
                "Which narrative element is most directly involved?"
            ),
            [
                "plot development",
                "setting",
                "rhyme scheme",
                "stage direction"
            ],
            0,
            "Prose",
            "Plot",
            (
                "Plot concerns the sequence and causal development "
                "of events in a narrative."
            )
        )

    if kind == "character":

        return add_question(
            "Literature",
            (
                "A character's actions repeatedly contradict what "
                "the character claims to believe. What does this "
                "most strongly reveal?"
            ),
            [
                "a conflict between stated values and behaviour",
                "the absence of characterization",
                "a fixed rhyme scheme",
                "a change in narrative setting"
            ],
            0,
            "Prose",
            "Characterization",
            (
                "Contradiction between speech and action can reveal "
                "complexity, conflict or unreliability."
            )
        )

    if kind == "theme":

        return add_question(
            "Literature",
            (
                "A novel repeatedly examines how excessive ambition "
                "causes a respected leader to make destructive decisions. "
                "Which theme is most clearly developed?"
            ),
            [
                "the destructive consequences of unchecked ambition",
                "the importance of weather",
                "the superiority of one setting",
                "the structure of rhyme"
            ],
            0,
            "Prose",
            "Theme",
            (
                "A recurring central idea concerning ambition and "
                "its consequences constitutes a theme."
            )
        )

    if kind == "irony":

        return add_question(
            "Literature",
            (
                "A character proudly announces that a plan cannot fail, "
                "while the audience already knows that the plan is "
                "about to collapse. This is an example of:"
            ),
            [
                "dramatic irony",
                "alliteration",
                "personification",
                "onomatopoeia"
            ],
            0,
            "Drama",
            "Irony",
            (
                "Dramatic irony occurs when the audience knows information "
                "that a character does not know."
            )
        )

    if kind == "imagery":

        return add_question(
            "Literature",
            (
                "A poet describes a sunset as 'a furnace of molten gold.' "
                "Which literary device is most prominent?"
            ),
            [
                "metaphor",
                "pun",
                "understatement",
                "litotes"
            ],
            0,
            "Poetry",
            "Figurative language",
            (
                "The sunset is directly identified with a furnace "
                "without using 'like' or 'as', creating a metaphor."
            )
        )

    if kind == "symbolism":

        return add_question(
            "Literature",
            (
                "In a story, a repeatedly locked door represents a "
                "character's inability to escape a restrictive past. "
                "The door functions primarily as a:"
            ),
            [
                "symbol",
                "rhyme",
                "stage direction",
                "narrative tense"
            ],
            0,
            "Prose",
            "Symbolism",
            (
                "A concrete object that represents an abstract idea "
                "functions symbolically."
            )
        )

    if kind == "dramatic":

        return add_question(
            "Literature",
            (
                "Why can a soliloquy be particularly useful in drama?"
            ),
            [
                "It can reveal a character's private thoughts directly to the audience.",
                "It prevents the audience from learning anything about the character.",
                "It removes all conflict from the play.",
                "It must always be delivered by every character."
            ],
            0,
            "Drama",
            "Soliloquy",
            (
                "A soliloquy gives direct access to a character's "
                "thoughts or reflections."
            )
        )

    if kind == "poetry":

        return add_question(
            "Literature",
            (
                "A poem repeatedly returns to the same phrase at "
                "the beginning of successive lines. This technique "
                "is most closely associated with:"
            ),
            [
                "repetition",
                "enjambment",
                "anticlimax",
                "foreshadowing"
            ],
            0,
            "Poetry",
            "Structure",
            (
                "Repetition deliberately repeats words or phrases "
                "for emphasis, rhythm or thematic effect."
            )
        )

    if kind == "narrative":

        return add_question(
            "Literature",
            (
                "A narrator describes events while knowing the thoughts "
                "and feelings of every major character. This is most "
                "consistent with:"
            ),
            [
                "omniscient narration",
                "first-person limited narration",
                "objective stage direction",
                "dramatic monologue"
            ],
            0,
            "Prose",
            "Narrative perspective",
            (
                "An omniscient narrator has broad knowledge of characters "
                "and events."
            )
        )

    return add_question(
        "Literature",
        (
            "A narrator describes a tragic event using cheerful, "
            "celebratory language. What effect can this contrast create?"
        ),
        [
            "ironic tension",
            "complete absence of tone",
            "literal neutrality",
            "chronological confusion"
        ],
        0,
        "Literary Appreciation",
        "Tone",
        (
            "A mismatch between subject matter and language can create "
            "ironic or unsettling tension."
        )
    )


# ============================================================
# 9. GEOGRAPHY
# ============================================================

def geography_generator():

    kind = random.choice([
        "climate",
        "population",
        "erosion",
        "river",
        "agriculture",
        "map",
        "weather",
        "industry",
        "urbanisation",
        "resources"
    ])

    if kind == "climate":

        return add_question(
            "Geography",
            (
                "Why do coastal areas often experience smaller "
                "annual temperature ranges than continental interiors?"
            ),
            [
                "Water heats and cools more slowly than land.",
                "Coastal regions receive no solar radiation.",
                "Land has no thermal capacity.",
                "Ocean water permanently blocks atmospheric circulation."
            ],
            0,
            "Climate",
            "Temperature",
            (
                "Water has a high heat capacity and moderates "
                "temperature changes."
            )
        )

    if kind == "population":

        return add_question(
            "Geography",
            (
                "A region has a high birth rate, falling death rate "
                "and improving healthcare. What demographic effect "
                "is most likely initially?"
            ),
            [
                "rapid population growth",
                "immediate population decline",
                "zero population growth",
                "complete migration out of the region"
            ],
            0,
            "Population",
            "Population growth",
            (
                "When births substantially exceed deaths, population "
                "growth occurs."
            )
        )

    if kind == "erosion":

        return add_question(
            "Geography",
            (
                "Which combination would most likely increase soil "
                "erosion on a steep cultivated slope?"
            ),
            [
                "removal of vegetation and intense rainfall",
                "terracing and contour farming",
                "dense vegetation and mulching",
                "windbreaks and cover crops"
            ],
            0,
            "Geomorphology",
            "Soil erosion",
            (
                "Vegetation protects soil, while intense rainfall and "
                "steep slopes increase runoff and erosion."
            )
        )

    if kind == "river":

        return add_question(
            "Geography",
            (
                "Why does a river commonly meander more strongly on "
                "a broad, low-gradient floodplain?"
            ),
            [
                "Lateral erosion and deposition become important.",
                "The river becomes completely stationary.",
                "Vertical erosion always becomes impossible.",
                "Rainfall ceases over floodplains."
            ],
            0,
            "Drainage",
            "River processes",
            (
                "Low gradients allow lateral erosion and deposition "
                "to shape pronounced bends."
            )
        )

    if kind == "agriculture":

        return add_question(
            "Geography",
            (
                "Which physical factor is most directly responsible "
                "for determining whether a crop can grow successfully "
                "in a particular climate?"
            ),
            [
                "temperature and moisture conditions",
                "political party membership",
                "road traffic volume",
                "population language"
            ],
            0,
            "Economic Geography",
            "Agriculture",
            (
                "Crops require suitable ranges of temperature and "
                "water availability."
            )
        )

    if kind == "map":

        return add_question(
            "Geography",
            (
                "On a map with scale 1:50,000, a road measures 4 cm. "
                "What is its actual ground distance?"
            ),
            [
                "2 km",
                "20 km",
                "200 m",
                "0.2 km"
            ],
            0,
            "Map Reading",
            "Scale",
            (
                "4 cm × 50,000 = 200,000 cm = 2 km."
            )
        )

    if kind == "weather":

        return add_question(
            "Geography",
            (
                "When warm moist air rises, cools and reaches saturation, "
                "which process can initiate cloud formation?"
            ),
            [
                "condensation",
                "sublimation only",
                "evaporation only",
                "infiltration"
            ],
            0,
            "Weather",
            "Cloud formation",
            (
                "Cooling moist air can reach saturation, allowing "
                "water vapour to condense around condensation nuclei."
            )
        )

    if kind == "industry":

        return add_question(
            "Geography",
            (
                "A factory that uses bulky raw materials that lose "
                "weight during processing is often attracted toward "
                "the source of the raw material because:"
            ),
            [
                "transporting the raw material is relatively costly",
                "labour is always unavailable in cities",
                "markets never influence industrial location",
                "all factories require identical locations"
            ],
            0,
            "Economic Geography",
            "Industrial location",
            (
                "Weight-losing industries may locate near raw materials "
                "to reduce transport costs."
            )
        )

    if kind == "urbanisation":

        return add_question(
            "Geography",
            (
                "Rapid urbanisation without adequate infrastructure "
                "is most likely to increase:"
            ),
            [
                "pressure on housing and urban services",
                "rural land availability",
                "agricultural productivity automatically",
                "the number of uninhabited urban areas"
            ],
            0,
            "Settlement",
            "Urbanisation",
            (
                "Rapid population concentration can place pressure "
                "on housing, transport, sanitation and other services."
            )
        )

    return add_question(
        "Geography",
        (
            "Why can a country with abundant mineral resources still "
            "experience limited economic benefit from them?"
        ),
        [
            "Extraction, infrastructure, technology and governance may constrain benefits.",
            "Mineral resources automatically guarantee prosperity.",
            "Minerals require no infrastructure to extract.",
            "Resource availability eliminates all economic risks."
        ],
        0,
        "Resources",
        "Mineral resources",
        (
            "Resource wealth does not automatically translate into "
            "development; institutions, infrastructure, technology "
            "and value addition matter."
        )
    )


# ============================================================
# 10. COMMERCE
# ============================================================

def commerce_generator():

    kind = random.choice([
        "trade",
        "insurance",
        "banking",
        "transport",
        "marketing",
        "warehousing",
        "business",
        "documents",
        "retailing",
        "entrepreneurship"
    ])

    if kind == "trade":

        return add_question(
            "Commerce",
            (
                "Why is international trade possible even when two "
                "countries can produce the same broad categories of goods?"
            ),
            [
                "Differences in relative costs and comparative advantage can create gains from trade.",
                "All countries have identical production costs.",
                "Trade requires every country to produce only one good.",
                "International trade eliminates scarcity."
            ],
            0,
            "Trade",
            "Comparative advantage",
            (
                "Differences in opportunity costs can make specialisation "
                "and exchange beneficial."
            )
        )

    if kind == "insurance":

        return add_question(
            "Commerce",
            (
                "The principle of indemnity in insurance is primarily "
                "intended to:"
            ),
            [
                "restore the insured financially to approximately the pre-loss position",
                "allow the insured to profit from every loss",
                "guarantee that accidents never occur",
                "eliminate the need for insurance contracts"
            ],
            0,
            "Insurance",
            "Principles of insurance",
            (
                "Indemnity aims to compensate for covered loss rather "
                "than create an opportunity for unjust enrichment."
            )
        )

    if kind == "banking":

        return add_question(
            "Commerce",
            (
                "When a commercial bank grants a loan and credits "
                "the borrower's deposit account, what broad banking "
                "function is being performed?"
            ),
            [
                "credit creation",
                "physical transportation",
                "warehousing",
                "retailing"
            ],
            0,
            "Banking",
            "Commercial banking",
            (
                "Commercial banks create deposits when extending "
                "credit under the banking system."
            )
        )

    if kind == "transport":

        return add_question(
            "Commerce",
            (
                "Which mode of transport is generally most suitable "
                "for moving very large quantities of bulky goods "
                "over long distances at relatively low unit cost?"
            ),
            [
                "water transport",
                "motorcycle transport",
                "air transport",
                "bicycle transport"
            ],
            0,
            "Transport",
            "Modes of transport",
            (
                "Water transport is often economical for heavy or "
                "bulky cargo over long distances."
            )
        )

    if kind == "marketing":

        return add_question(
            "Commerce",
            (
                "A company studies customer preferences before launching "
                "a new product. What marketing activity is it primarily "
                "undertaking?"
            ),
            [
                "market research",
                "warehousing",
                "bookkeeping",
                "transportation"
            ],
            0,
            "Marketing",
            "Market research",
            (
                "Market research gathers information about customers, "
                "competitors and market conditions."
            )
        )

    if kind == "warehousing":

        return add_question(
            "Commerce",
            (
                "Which commercial function of warehousing allows a "
                "business to hold goods until they are needed?"
            ),
            [
                "storage",
                "negotiation",
                "advertising",
                "auditing"
            ],
            0,
            "Warehousing",
            "Functions",
            (
                "Storage allows goods to be preserved until distribution "
                "or sale."
            )
        )

    if kind == "business":

        return add_question(
            "Commerce",
            (
                "Which characteristic most directly distinguishes a "
                "limited liability company from a sole proprietorship?"
            ),
            [
                "owners generally have limited liability for company debts",
                "it can never make a profit",
                "it has no legal identity",
                "it cannot enter contracts"
            ],
            0,
            "Business Organisation",
            "Limited liability",
            (
                "Limited liability generally protects owners' personal "
                "assets from business debts, subject to the law."
            )
        )

    if kind == "documents":

        return add_question(
            "Commerce",
            (
                "Which document commonly provides evidence that goods "
                "have been dispatched by a carrier?"
            ),
            [
                "consignment note",
                "balance sheet",
                "share certificate",
                "memorandum of association"
            ],
            0,
            "Trade Documents",
            "Transportation documents",
            (
                "A consignment note records details associated with "
                "goods entrusted to a carrier."
            )
        )

    if kind == "retailing":

        return add_question(
            "Commerce",
            (
                "A retailer buys goods in relatively small quantities "
                "from wholesalers and sells them to final consumers. "
                "Which role is being performed?"
            ),
            [
                "breaking bulk",
                "manufacturing",
                "mining",
                "insurance underwriting"
            ],
            0,
            "Retail Trade",
            "Functions of retailers",
            (
                "Retailers often break bulk by purchasing larger "
                "quantities and selling smaller units to consumers."
            )
        )

    return add_question(
        "Commerce",
        (
            "An entrepreneur identifies an unmet customer need and "
            "organises resources to provide a solution. Which role "
            "is most clearly demonstrated?"
        ),
        [
            "innovation and risk-bearing",
            "passive consumption",
            "government taxation",
            "inventory destruction"
        ],
        0,
        "Entrepreneurship",
        "Entrepreneurial functions",
        (
            "Entrepreneurs identify opportunities, organise resources "
            "and bear business risks."
        )
    )


# ============================================================
# 11. ACCOUNTING
# ============================================================

def accounting_generator():

    kind = random.choice([
        "accounting_equation",
        "depreciation",
        "profit",
        "inventory",
        "capital",
        "bank_reconciliation",
        "trial_balance",
        "ratio",
        "double_entry",
        "cash_flow"
    ])

    if kind == "accounting_equation":

        assets = random.randint(
            100000,
            900000
        )

        liabilities = random.randint(
            20000,
            assets // 2
        )

        capital = assets - liabilities

        return add_question(
            "Accounting",
            (
                f"A business has total assets of ₦{assets:,} "
                f"and liabilities of ₦{liabilities:,}. "
                "What is the owner's equity?"
            ),
            [
                f"₦{capital:,}",
                f"₦{assets + liabilities:,}",
                f"₦{liabilities:,}",
                f"₦{assets - capital:,}"
            ],
            0,
            "Basic Accounting",
            "Accounting equation",
            (
                "Capital = Assets − Liabilities."
            )
        )

    if kind == "depreciation":

        cost = random.choice([
            200000,
            300000,
            500000,
            800000,
            1000000
        ])

        residual = random.choice([
            20000,
            50000,
            100000
        ])

        life = random.randint(
            4,
            10
        )

        annual = (
            cost - residual
        ) / life

        return add_question(
            "Accounting",
            (
                f"Using straight-line depreciation, calculate the "
                f"annual depreciation of an asset costing ₦{cost:,}, "
                f"with residual value ₦{residual:,} and useful life "
                f"of {life} years."
            ),
            [
                f"₦{annual:,.2f}",
                f"₦{cost / life:,.2f}",
                f"₦{(cost + residual) / life:,.2f}",
                f"₦{residual / life:,.2f}"
            ],
            0,
            "Non-current Assets",
            "Depreciation",
            (
                "Straight-line depreciation = "
                "(cost − residual value) / useful life."
            )
        )

    if kind == "profit":

        revenue = random.randint(
            500000,
            2000000
        )

        expenses = random.randint(
            100000,
            600000
        )

        profit = revenue - expenses

        return add_question(
            "Accounting",
            (
                f"A business records revenue of ₦{revenue:,} "
                f"and total expenses of ₦{expenses:,}. "
                "Ignoring tax, what is its profit?"
            ),
            [
                f"₦{profit:,}",
                f"₦{revenue + expenses:,}",
                f"₦{expenses:,}",
                f"₦{revenue:,}"
            ],
            0,
            "Financial Statements",
            "Profit",
            (
                "Profit is revenue minus expenses."
            )
        )

    if kind == "inventory":

        opening = random.randint(
            100000,
            400000
        )

        purchases = random.randint(
            200000,
            700000
        )

        closing = random.randint(
            50000,
            300000
        )

        cost_sales = (
            opening +
            purchases -
            closing
        )

        return add_question(
            "Accounting",
            (
                f"Opening inventory is ₦{opening:,}, purchases are "
                f"₦{purchases:,}, and closing inventory is "
                f"₦{closing:,}. Calculate cost of goods sold."
            ),
            [
                f"₦{cost_sales:,}",
                f"₦{opening + purchases + closing:,}",
                f"₦{purchases - closing:,}",
                f"₦{closing:,}"
            ],
            0,
            "Final Accounts",
            "Cost of goods sold",
            (
                "COGS = opening inventory + purchases − closing inventory."
            )
        )

    if kind == "capital":

        return add_question(
            "Accounting",
            (
                "Which transaction increases both the assets and "
                "owner's capital of a business?"
            ),
            [
                "The owner introduces additional cash into the business.",
                "The business pays a creditor.",
                "The business withdraws cash for personal use.",
                "The business writes off an irrecoverable debt."
            ],
            0,
            "Capital",
            "Capital transactions",
            (
                "Introducing additional owner funds increases cash "
                "and owner's equity."
            )
        )

    if kind == "bank_reconciliation":

        return add_question(
            "Accounting",
            (
                "A cheque issued by a business has not yet been "
                "presented to the bank. What is the usual effect "
                "when reconciling the cash book with the bank statement?"
            ),
            [
                "The bank statement balance may be higher than the adjusted cash book balance.",
                "The bank statement must become zero.",
                "The cheque automatically becomes revenue.",
                "The transaction is treated as depreciation."
            ],
            0,
            "Bank Reconciliation",
            "Unpresented cheques",
            (
                "An unpresented cheque has reduced the cash book "
                "but has not yet reduced the bank statement balance."
            )
        )

    if kind == "trial_balance":

        return add_question(
            "Accounting",
            (
                "Which error may not cause a trial balance to disagree?"
            ),
            [
                "an error of complete omission",
                "a single-sided posting error",
                "incorrect addition of one side",
                "posting different amounts to debit and credit"
            ],
            0,
            "Trial Balance",
            "Errors",
            (
                "If a transaction is completely omitted, neither "
                "debit nor credit is recorded, so the trial balance "
                "can still balance."
            )
        )

    if kind == "ratio":

        current_assets = random.randint(
            500000,
            1500000
        )

        current_liabilities = random.randint(
            250000,
            800000
        )

        ratio = (
            current_assets /
            current_liabilities
        )

        return add_question(
            "Accounting",
            (
                f"A company has current assets of ₦{current_assets:,} "
                f"and current liabilities of ₦{current_liabilities:,}. "
                "What is its current ratio approximately?"
            ),
            [
                f"{ratio:.2f}:1",
                f"{current_liabilities / current_assets:.2f}:1",
                f"{current_assets + current_liabilities}:1",
                f"{current_assets - current_liabilities}:1"
            ],
            0,
            "Accounting Ratios",
            "Current ratio",
            (
                "Current ratio = current assets / current liabilities."
            )
        )

    if kind == "double_entry":

        return add_question(
            "Accounting",
            (
                "A business purchases office furniture for cash. "
                "Which accounts are affected?"
            ),
            [
                "Furniture is debited and Cash is credited.",
                "Cash is debited and Furniture is credited.",
                "Sales is debited and Cash is credited.",
                "Capital is debited and Furniture is credited."
            ],
            0,
            "Double Entry",
            "Asset transactions",
            (
                "Furniture increases and is debited; cash decreases "
                "and is credited."
            )
        )

    return add_question(
        "Accounting",
        (
            "Which statement best describes a cash flow statement?"
        ),
        [
            "It reports movements in cash and cash equivalents over a period.",
            "It records only the physical assets owned by a business.",
            "It replaces every other financial statement.",
            "It records only credit sales."
        ],
        0,
        "Financial Statements",
        "Cash flow",
        (
            "A cash flow statement explains cash inflows and outflows "
            "during an accounting period."
        )
    )


# ============================================================
# 12. AGRICULTURAL SCIENCE
# ============================================================

def agricultural_science_generator():

    kind = random.choice([
        "soil",
        "livestock",
        "crop",
        "farm_management",
        "pests",
        "irrigation",
        "breeding",
        "nutrition",
        "conservation",
        "economics"
    ])

    if kind == "soil":

        return add_question(
            "Agricultural Science",
            (
                "Which soil property most directly affects the amount "
                "of water and nutrients that can be retained for plants?"
            ),
            [
                "texture and structure",
                "colour alone",
                "geographical name",
                "field boundary length"
            ],
            0,
            "Soil Science",
            "Soil properties",
            (
                "Soil texture and structure influence pore spaces, "
                "drainage, aeration and nutrient retention."
            )
        )

    if kind == "livestock":

        return add_question(
            "Agricultural Science",
            (
                "Why is adequate ventilation important in intensive "
                "livestock housing?"
            ),
            [
                "It helps remove excess heat, moisture and harmful gases.",
                "It prevents animals from requiring water.",
                "It eliminates the need for feeding.",
                "It stops all diseases completely."
            ],
            0,
            "Animal Husbandry",
            "Housing",
            (
                "Ventilation supports suitable temperature, humidity "
                "and air quality."
            )
        )

    if kind == "crop":

        return add_question(
            "Agricultural Science",
            (
                "A farmer plants legumes in rotation with a cereal crop. "
                "What is a major potential benefit?"
            ),
            [
                "Improved soil nitrogen availability through biological fixation.",
                "Permanent elimination of all weeds.",
                "Complete prevention of soil erosion.",
                "Removal of every soil microorganism."
            ],
            0,
            "Crop Production",
            "Crop rotation",
            (
                "Legumes can form symbiotic relationships with nitrogen-fixing "
                "bacteria, contributing nitrogen to the system."
            )
        )

    if kind == "farm_management":

        return add_question(
            "Agricultural Science",
            (
                "A farmer compares expected revenue with variable and "
                "fixed costs before deciding whether to expand production. "
                "Which management process is being demonstrated?"
            ),
            [
                "economic planning",
                "animal vaccination",
                "seed dormancy",
                "pollination"
            ],
            0,
            "Farm Management",
            "Farm planning",
            (
                "Economic planning evaluates expected costs, revenue "
                "and profitability before decisions are made."
            )
        )

    if kind == "pests":

        return add_question(
            "Agricultural Science",
            (
                "Why is integrated pest management often preferred "
                "to relying exclusively on chemical pesticides?"
            ),
            [
                "It combines several control methods and can reduce excessive pesticide use.",
                "It requires farmers to ignore pest populations.",
                "It guarantees that every insect is destroyed.",
                "It eliminates the need for monitoring."
            ],
            0,
            "Crop Protection",
            "Integrated pest management",
            (
                "IPM combines biological, cultural, mechanical and "
                "carefully selected chemical methods."
            )
        )

    if kind == "irrigation":

        return add_question(
            "Agricultural Science",
            (
                "Which irrigation method delivers water slowly and "
                "directly near the root zone of individual plants?"
            ),
            [
                "drip irrigation",
                "flood irrigation",
                "wild flooding",
                "overland flow"
            ],
            0,
            "Farm Water Management",
            "Irrigation",
            (
                "Drip systems deliver controlled quantities of water "
                "near plant roots."
            )
        )

    if kind == "breeding":

        return add_question(
            "Agricultural Science",
            (
                "The deliberate mating of selected animals to combine "
                "desirable inherited characteristics is known as:"
            ),
            [
                "selective breeding",
                "random grazing",
                "soil tillage",
                "crop harvesting"
            ],
            0,
            "Animal Improvement",
            "Breeding",
            (
                "Selective breeding chooses parents with desirable "
                "traits to influence offspring characteristics."
            )
        )

    if kind == "nutrition":

        return add_question(
            "Agricultural Science",
            (
                "Which nutrient is particularly important for tissue "
                "growth and repair in livestock?"
            ),
            [
                "protein",
                "water only",
                "fibre only",
                "mineral salts only"
            ],
            0,
            "Animal Nutrition",
            "Feed nutrients",
            (
                "Protein supplies amino acids required for growth "
                "and tissue repair."
            )
        )

    if kind == "conservation":

        return add_question(
            "Agricultural Science",
            (
                "Which practice is most suitable for reducing soil "
                "erosion on steep cultivated land?"
            ),
            [
                "terracing",
                "complete removal of vegetation",
                "continuous bare-soil cultivation",
                "cultivation up and down the slope"
            ],
            0,
            "Soil Conservation",
            "Erosion control",
            (
                "Terracing reduces slope length and slows runoff."
            )
        )

    return add_question(
        "Agricultural Science",
        (
            "Why should a farmer keep accurate farm records?"
        ),
        [
            "They support planning, cost analysis and evaluation of farm performance.",
            "They guarantee that weather conditions never change.",
            "They eliminate every production risk.",
            "They make markets unnecessary."
        ],
        0,
        "Farm Management",
        "Record keeping",
        (
            "Records provide information needed for financial analysis, "
            "planning and decision-making."
        )
    )


# ============================================================
# 13. COMPUTER SCIENCE
# ============================================================

def computer_science_generator():

    kind = random.choice([
        "algorithm",
        "logic",
        "database",
        "network",
        "programming",
        "security",
        "data",
        "operating_system",
        "complexity",
        "architecture"
    ])

    if kind == "algorithm":

        return add_question(
            "Computer Science",
            (
                "An algorithm repeatedly divides a search interval "
                "into approximately equal halves when locating an "
                "item in a sorted list. Which algorithm is being described?"
            ),
            [
                "binary search",
                "linear search",
                "bubble sort",
                "depth-first traversal"
            ],
            0,
            "Algorithms",
            "Searching",
            (
                "Binary search repeatedly halves the search interval "
                "and requires sorted data."
            )
        )

    if kind == "logic":

        return add_question(
            "Computer Science",
            (
                "If A is True and B is False, what is the result of "
                "the Boolean expression A AND NOT B?"
            ),
            [
                "True",
                "False",
                "Undefined",
                "Both true and false"
            ],
            0,
            "Logic",
            "Boolean algebra",
            (
                "NOT B is True because B is False. "
                "True AND True is True."
            )
        )

    if kind == "database":

        return add_question(
            "Computer Science",
            (
                "In a relational database, what is the principal "
                "purpose of a primary key?"
            ),
            [
                "to uniquely identify each record in a table",
                "to store every possible duplicate record",
                "to replace all foreign keys",
                "to encrypt the entire database automatically"
            ],
            0,
            "Database",
            "Keys",
            (
                "A primary key uniquely identifies records within "
                "a relational table."
            )
        )

    if kind == "network":

        return add_question(
            "Computer Science",
            (
                "Which device primarily forwards packets between "
                "different networks?"
            ),
            [
                "router",
                "keyboard",
                "monitor",
                "printer"
            ],
            0,
            "Networking",
            "Network devices",
            (
                "Routers forward packets between networks based "
                "on network-layer information."
            )
        )

    if kind == "programming":

        return add_question(
            "Computer Science",
            (
                "A program uses a loop that continues while a "
                "condition remains true. What is the principal "
                "risk if the condition can never become false?"
            ),
            [
                "an infinite loop",
                "automatic compilation",
                "lossless compression",
                "normal termination"
            ],
            0,
            "Programming",
            "Control structures",
            (
                "A loop whose termination condition is never reached "
                "can execute indefinitely."
            )
        )

    if kind == "security":

        return add_question(
            "Computer Science",
            (
                "An attacker sends a deceptive message designed to "
                "trick a user into revealing a password. This is "
                "best described as:"
            ),
            [
                "phishing",
                "defragmentation",
                "compilation",
                "load balancing"
            ],
            0,
            "Cybersecurity",
            "Social engineering",
            (
                "Phishing uses deceptive communications to obtain "
                "sensitive information."
            )
        )

    if kind == "data":

        return add_question(
            "Computer Science",
            (
                "Which data structure follows the Last-In, First-Out "
                "principle?"
            ),
            [
                "stack",
                "queue",
                "array only",
                "graph"
            ],
            0,
            "Data Structures",
            "Stacks",
            (
                "A stack removes the most recently inserted item first."
            )
        )

    if kind == "operating_system":

        return add_question(
            "Computer Science",
            (
                "Which operating-system function is responsible for "
                "allocating processor time among competing processes?"
            ),
            [
                "CPU scheduling",
                "screen resolution",
                "file naming only",
                "keyboard manufacture"
            ],
            0,
            "Operating Systems",
            "Process management",
            (
                "The scheduler determines which ready process gets "
                "CPU time."
            )
        )

    if kind == "complexity":

        return add_question(
            "Computer Science",
            (
                "An algorithm examines each of n elements exactly once. "
                "What is its dominant time complexity?"
            ),
            [
                "O(n)",
                "O(1)",
                "O(n²)",
                "O(2ⁿ)"
            ],
            0,
            "Algorithms",
            "Complexity",
            (
                "A single pass through n elements grows linearly "
                "with n, giving O(n)."
            )
        )

    return add_question(
        "Computer Science",
        (
            "Which component temporarily stores data and instructions "
            "that the CPU is actively using?"
        ),
        [
            "RAM",
            "hard disk enclosure",
            "keyboard",
            "power supply"
        ],
        0,
        "Computer Architecture",
        "Memory",
        (
            "RAM provides fast temporary storage for actively used "
            "program instructions and data."
        )
    )


# ============================================================
# GENERATOR REGISTRY
# ============================================================

GENERATORS = {
    "Use of English": english_generator,
    "Mathematics": mathematics_generator,
    "Physics": physics_generator,
    "Chemistry": chemistry_generator,
    "Biology": biology_generator,
    "Economics": economics_generator,
    "Government": government_generator,
    "Literature": literature_generator,
    "Geography": geography_generator,
    "Commerce": commerce_generator,
    "Accounting": accounting_generator,
    "Agricultural Science": agricultural_science_generator,
    "Computer Science": computer_science_generator,
}


# ============================================================
# VALIDATION
# ============================================================

def validate_generators():

    missing = [
        subject
        for subject in SUBJECTS
        if subject not in GENERATORS
    ]

    if missing:

        raise RuntimeError(
            "Missing generators for: "
            + ", ".join(missing)
        )

    print(
        f"Validated {len(GENERATORS)} subject generators.",
        flush=True
    )


# ============================================================
# MAIN SEED FUNCTION
# ============================================================

def run():

    random.seed(RANDOM_SEED)

    print("=" * 78)
    print(
        "CAREER BRIDGE — EXTREME JAMB-STYLE QUESTION BANK"
    )
    print(
        f"Target: {TARGET_PER_SUBJECT} questions per subject"
    )
    print(
        f"Subjects: {len(SUBJECTS)}"
    )
    print(
        f"Total target: "
        f"{TARGET_PER_SUBJECT * len(SUBJECTS)}"
    )
    print(
        "Difficulty: EXTREME"
    )
    print("=" * 78)

    with app.app_context():

        validate_generators()

        cleanup_legacy_generated_questions()

        before_total = JAMBQuestion.query.count()

        for subject in SUBJECTS:

            before = count_subject(subject)

            if before >= TARGET_PER_SUBJECT:

                print(
                    f"{subject}: {before} already present — skipped.",
                    flush=True
                )

                continue

            print(
                f"\nGenerating {subject}: "
                f"{before} -> {TARGET_PER_SUBJECT}",
                flush=True
            )

            generator = GENERATORS[subject]

            add_until(
                subject,
                TARGET_PER_SUBJECT,
                generator
            )

            after = count_subject(subject)

            print(
                f"{subject}: {before} -> {after}",
                flush=True
            )

        after_total = JAMBQuestion.query.count()

        print("\n" + "=" * 78)
        print(
            f"Question bank before: {before_total}"
        )
        print(
            f"Question bank after:  {after_total}"
        )
        print("=" * 78)

        print("\nSUBJECT COUNTS:")

        for subject in SUBJECTS:

            print(
                f"{subject}: "
                f"{count_subject(subject)}"
            )

        print(
            "\nSeeding complete.",
            flush=True
        )


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":
    run()
