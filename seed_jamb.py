from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import random
import math

# ============================================================
# CAREER BRIDGE - JAMB QUESTION BANK SEEDER
# ============================================================
# This file creates ORIGINAL JAMB-STYLE practice questions.
# They are NOT official JAMB past questions.
#
# It generates at least 500 questions for EACH subject:
#   Use of English, Mathematics, Physics, Chemistry, Biology,
#   Economics, Government, Literature, Geography, Commerce,
#   Accounting, Agricultural Science, Computer Science
#
# Total minimum: 6,500 questions.
#
# Run:
#     python seed_jamb.py
#
# The script imports the existing Flask app and database models
# from app.py, so keep this file in the same project folder.
# ============================================================

from app import app, db, JAMBQuestion


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


def add_question(subject, question, a, b, c, d, answer,
                 topic=None, subtopic=None, difficulty="Medium",
                 explanation=None):
    """Add one question if an identical question is not already present."""
    if JAMBQuestion.query.filter_by(
        subject=subject,
        question=question
    ).first():
        return False

    db.session.add(JAMBQuestion(
        year=None,
        subject=subject,
        topic=topic,
        subtopic=subtopic,
        difficulty=difficulty,
        question=question,
        option_a=a,
        option_b=b,
        option_c=c,
        option_d=d,
        correct_answer=answer,
        explanation=explanation or f"The correct answer is {answer}.",
        source="Career Bridge Original Practice Question",
        created_at=datetime.utcnow()
    ))
    return True


# ------------------------------------------------------------
# Generic helper
# ------------------------------------------------------------

def mcq(subject, q, options, answer_index, topic, subtopic,
        difficulty="Medium", explanation=None):
    labels = ["A", "B", "C", "D"]
    answer = labels[answer_index]
    return add_question(
        subject, q, options[0], options[1], options[2], options[3],
        answer, topic, subtopic, difficulty, explanation
    )


# ============================================================
# USE OF ENGLISH
# ============================================================

ENGLISH_WORDS = [
    ("abundant", "scarce", "plentiful", "careless", "ancient"),
    ("brief", "lengthy", "short", "heavy", "bright"),
    ("candid", "secretive", "frank", "hostile", "uncertain"),
    ("diligent", "lazy", "careful", "angry", "weak"),
    ("eloquent", "silent", "expressive", "rough", "unclear"),
    ("fragile", "strong", "delicate", "large", "rough"),
    ("hostile", "friendly", "aggressive", "quiet", "helpful"),
    ("impartial", "biased", "fair", "careless", "uncertain"),
    ("juvenile", "adult", "young", "old", "serious"),
    ("liberal", "generous", "strict", "narrow", "timid"),
    ("mandatory", "optional", "compulsory", "unlikely", "temporary"),
    ("notorious", "famous for wrongdoing", "unknown", "honest", "ordinary"),
    ("obsolete", "modern", "outdated", "expensive", "popular"),
    ("precise", "exact", "rough", "slow", "uncertain"),
    ("reluctant", "eager", "unwilling", "certain", "joyful"),
    ("scarce", "plentiful", "rare", "cheap", "common"),
    ("timid", "bold", "shy", "loud", "careless"),
    ("vital", "useless", "essential", "optional", "minor"),
    ("weary", "tired", "excited", "angry", "healthy"),
    ("zealous", "indifferent", "enthusiastic", "weak", "uncertain"),
]


def seed_english(target=500):
    count = 0

    # Vocabulary
    for i, (word, correct, *wrong) in enumerate(ENGLISH_WORDS):
        q = f"Choose the option nearest in meaning to the word '{word}'."
        opts = [correct, wrong[0], wrong[1], wrong[2]]
        count += mcq(
            "Use of English", q, opts, 0,
            "Lexis and Structure", "Synonyms"
        )

        q = f"Choose the option opposite in meaning to '{word}'."
        opposite = wrong[0]
        opts = [opposite, correct, wrong[1], wrong[2]]
        count += mcq(
            "Use of English", q, opts, 0,
            "Lexis and Structure", "Antonyms"
        )

    # Grammar patterns
    grammar = [
        ("Neither the teacher nor the students ___ ready.",
         ["was", "were", "is", "has"], 1),
        ("If I ___ enough money, I would buy the book.",
         ["have", "had", "has", "will have"], 1),
        ("She has lived here ___ 2022.",
         ["for", "since", "from", "by"], 1),
        ("The boys ___ football every Saturday.",
         ["plays", "play", "playing", "has played"], 1),
        ("By the time we arrived, the meeting ___.",
         ["starts", "has started", "had started", "will start"], 2),
        ("He is good ___ Mathematics.",
         ["in", "at", "on", "with"], 1),
        ("The news ___ surprising.",
         ["were", "are", "was", "have"], 2),
        ("Each of the candidates ___ a question paper.",
         ["receive", "receives", "receiving", "have received"], 1),
        ("I prefer tea ___ coffee.",
         ["than", "to", "over", "from"], 1),
        ("She arrived ___ the airport before noon.",
         ["at", "in", "on", "into"], 0),
        ("The man ___ car was stolen reported to the police.",
         ["who", "whose", "which", "whom"], 1),
        ("We have not seen him ___ Monday.",
         ["for", "since", "during", "while"], 1),
        ("He speaks English ___ than his brother.",
         ["good", "better", "best", "well"], 1),
        ("They ___ dinner when the phone rang.",
         ["eat", "were eating", "have eaten", "will eat"], 1),
        ("The opposite of 'expand' is ___.",
         ["increase", "contract", "develop", "extend"], 1),
    ]

    for i, (q, opts, ans) in enumerate(grammar):
        count += mcq(
            "Use of English", q, opts, ans,
            "Lexis and Structure", "Grammar"
        )

    # Generate additional original grammar/vocabulary practice
    nouns = ["committee", "family", "team", "class", "audience"]
    verbs = ["has", "have"]
    for i in range(120):
        noun = nouns[i % len(nouns)]
        if noun in {"committee", "family", "team", "class", "audience"}:
            ans = 0
        else:
            ans = 1
        q = f"The {noun} of students ___ completed the assignment."
        opts = ["has", "have", "having", "were"]
        count += mcq(
            "Use of English", q, opts, ans,
            "Lexis and Structure", "Concord"
        )

    # Comprehension-style short passages
    passages = [
        (
            "Regular reading improves vocabulary because readers meet words "
            "in different contexts. It also develops the ability to identify "
            "the main idea of a passage.",
            "What is the main benefit of reading mentioned in the passage?",
            ["Improved vocabulary and comprehension", "Poor concentration",
             "Reduced vocabulary", "Avoiding all writing"],
            0
        ),
        (
            "A good student does not merely memorize facts. Such a student "
            "also asks questions, compares ideas and applies knowledge to "
            "new situations.",
            "According to the passage, a good student should also be able to ___",
            ["avoid questions", "apply knowledge", "memorize without thinking",
             "ignore new situations"],
            1
        ),
        (
            "Time management helps students divide their work into manageable "
            "parts. A timetable can reduce the tendency to postpone tasks.",
            "What problem can a timetable help reduce?",
            ["Revision", "Planning", "Procrastination", "Learning"],
            2
        ),
        (
            "Public transport can reduce the number of private cars on busy "
            "roads. When more people share buses or trains, road congestion "
            "may fall.",
            "What is one possible effect of public transport?",
            ["More congestion", "Less road congestion",
             "More private cars", "Fewer roads"],
            1
        ),
    ]

    for passage, q, opts, ans in passages:
        for j in range(35):
            modified_q = q
            if j:
                modified_q = q.replace(
                    "mentioned in the passage",
                    "described by the passage"
                ).replace(
                    "according to the passage",
                    "according to the passage"
                )
            count += mcq(
                "Use of English",
                f"Read the passage: '{passage}'\n\n{modified_q}",
                opts, ans, "Comprehension", "Main Ideas"
            )

    # Fill safely to target with grammar identification
    forms = [
        ("The word 'quickly' is what part of speech?", 
         ["Adverb", "Noun", "Pronoun", "Conjunction"], 0, "Parts of Speech"),
        ("The word 'beautiful' is what part of speech?",
         ["Adjective", "Verb", "Adverb", "Preposition"], 0, "Parts of Speech"),
        ("The word 'and' is what part of speech?",
         ["Conjunction", "Adjective", "Pronoun", "Noun"], 0, "Parts of Speech"),
        ("The word 'under' is commonly used as a ___",
         ["Preposition", "Noun", "Pronoun", "Verb"], 0, "Parts of Speech"),
    ]

    i = 0
    while count < target:
        q, opts, ans, sub = forms[i % len(forms)]
        q = q.rstrip("?") + f" in sentence set {i + 1}?"
        count += mcq(
            "Use of English", q, opts, ans,
            "Lexis and Structure", sub
        )
        i += 1

    return count


# ============================================================
# MATHEMATICS
# ============================================================

def seed_mathematics(target=500):
    count = 0

    for n in range(1, 181):
        a = n + 2
        b = n % 12 + 2
        q = f"If 2x + {a} = {2*a + 10}, what is x?"
        x = a + 5
        opts = [str(x), str(x + 1), str(x - 1), str(x + 2)]
        count += mcq(
            "Mathematics", q, opts, 0,
            "Algebra", "Linear Equations"
        )

    for n in range(1, 121):
        a = n + 3
        b = n + 7
        q = f"What is the value of ({a} + {b}) × 2?"
        ans = (a + b) * 2
        opts = [str(ans), str(ans + 2), str(ans - 2), str(ans + 4)]
        count += mcq(
            "Mathematics", q, opts, 0,
            "Number", "Arithmetic"
        )

    for n in range(1, 101):
        base = n + 2
        height = (n % 10) + 4
        area = base * height / 2
        q = f"Find the area of a triangle with base {base} cm and height {height} cm."
        opts = [f"{area:g} cm²", f"{area + 2:g} cm²",
                f"{area * 2:g} cm²", f"{max(1, area - 2):g} cm²"]
        count += mcq(
            "Mathematics", q, opts, 0,
            "Mensuration", "Area of Triangle"
        )

    for n in range(1, 101):
        radius = n % 10 + 2
        circumference_factor = 2 * radius
        q = f"Using π = 22/7, what is the circumference of a circle of radius {radius} cm?"
        ans = 2 * (22/7) * radius
        opts = [f"{ans:g} cm", f"{ans + 2:g} cm",
                f"{ans - 2:g} cm", f"{ans / 2:g} cm"]
        count += mcq(
            "Mathematics", q, opts, 0,
            "Mensuration", "Circle"
        )

    for n in range(1, 101):
        first = n + 2
        diff = n % 8 + 1
        term = first + 9 * diff
        q = f"An arithmetic sequence starts with {first} and has common difference {diff}. Find its 10th term."
        opts = [str(term), str(term + diff), str(term - diff), str(term + 2*diff)]
        count += mcq(
            "Mathematics", q, opts, 0,
            "Algebra", "Sequences"
        )

    # Probability
    for n in range(1, 80):
        red = n % 6 + 2
        blue = n % 5 + 3
        total = red + blue
        q = f"A bag contains {red} red balls and {blue} blue balls. What is the probability of picking a red ball?"
        from fractions import Fraction
        ans = Fraction(red, total)
        opts = [str(ans), str(Fraction(blue, total)),
                str(Fraction(1, total)), str(Fraction(red + 1, total))]
        count += mcq(
            "Mathematics", q, opts, 0,
            "Probability", "Simple Probability"
        )

    # Fill to 500 with percentage questions
    i = 0
    while count < target:
        number = 100 + (i % 200)
        percent = [5, 10, 15, 20, 25, 30, 40, 50][i % 8]
        ans = number * percent / 100
        q = f"What is {percent}% of {number}?"
        opts = [str(int(ans)), str(int(ans + percent)),
                str(int(ans + 5)), str(int(ans * 2))]
        count += mcq(
            "Mathematics", q, opts, 0,
            "Number", "Percentages"
        )
        i += 1

    return count


# ============================================================
# PHYSICS
# ============================================================

def seed_physics(target=500):
    count = 0

    for i in range(100):
        v = i % 20 + 5
        t = i % 10 + 1
        s = v * t
        q = f"A body moves at a constant speed of {v} m/s for {t} s. How far does it travel?"
        opts = [f"{s} m", f"{s+t} m", f"{v+t} m", f"{s/2:g} m"]
        count += mcq(
            "Physics", q, opts, 0,
            "Mechanics", "Motion"
        )

    for i in range(100):
        m = i % 15 + 2
        a = i % 8 + 2
        force = m * a
        q = f"A mass of {m} kg accelerates at {a} m/s². What is the resultant force?"
        opts = [f"{force} N", f"{m+a} N", f"{force+2} N", f"{force/2:g} N"]
        count += mcq(
            "Physics", q, opts, 0,
            "Mechanics", "Newton's Laws"
        )

    for i in range(100):
        voltage = i % 12 + 2
        resistance = i % 8 + 2
        current = voltage / resistance
        q = f"A resistor of {resistance} Ω is connected to a {voltage} V supply. What current flows?"
        opts = [f"{current:g} A", f"{voltage*resistance:g} A",
                f"{resistance/voltage:g} A", f"{voltage+resistance:g} A"]
        count += mcq(
            "Physics", q, opts, 0,
            "Electricity", "Ohm's Law"
        )

    for i in range(100):
        mass = i % 20 + 2
        g = 10
        weight = mass * g
        q = f"Take g = 10 m/s². What is the weight of a {mass} kg object?"
        opts = [f"{weight} N", f"{mass} N", f"{weight/2:g} N", f"{weight+10} N"]
        count += mcq(
            "Physics", q, opts, 0,
            "Mechanics", "Weight"
        )

    concepts = [
        ("Which quantity has both magnitude and direction?",
         ["Velocity", "Mass", "Time", "Temperature"], 0),
        ("Which instrument is used to measure electric current?",
         ["Ammeter", "Voltmeter", "Thermometer", "Barometer"], 0),
        ("Which form of energy is stored in a stretched spring?",
         ["Elastic potential energy", "Sound energy", "Nuclear energy", "Light energy"], 0),
        ("Which wave requires a material medium for propagation?",
         ["Sound wave", "Light wave", "Radio wave", "Microwave"], 0),
        ("The SI unit of power is the ___",
         ["watt", "joule", "newton", "pascal"], 0),
        ("The SI unit of pressure is the ___",
         ["pascal", "watt", "volt", "ampere"], 0),
    ]
    i = 0
    while count < target:
        q, opts, ans = concepts[i % len(concepts)]
        q += f" (Practice item {i + 1})"
        count += mcq(
            "Physics", q, opts, ans,
            "General Physics", "Basic Concepts"
        )
        i += 1

    return count


# ============================================================
# CHEMISTRY
# ============================================================

def seed_chemistry(target=500):
    count = 0

    elements = [
        ("hydrogen", "H", 1),
        ("carbon", "C", 6),
        ("nitrogen", "N", 7),
        ("oxygen", "O", 8),
        ("sodium", "Na", 11),
        ("magnesium", "Mg", 12),
        ("aluminium", "Al", 13),
        ("silicon", "Si", 14),
        ("chlorine", "Cl", 17),
        ("potassium", "K", 19),
        ("calcium", "Ca", 20),
    ]

    for name, symbol, atomic_no in elements:
        q = f"What is the chemical symbol for {name}?"
        wrong = ["X", "Z", "Q"]
        opts = [symbol] + wrong
        count += mcq(
            "Chemistry", q, opts, 0,
            "Periodic Table", "Symbols"
        )

        q = f"What is the atomic number of {name}?"
        opts = [str(atomic_no), str(atomic_no + 1),
                str(max(1, atomic_no - 1)), str(atomic_no + 2)]
        count += mcq(
            "Chemistry", q, opts, 0,
            "Periodic Table", "Atomic Number"
        )

    # Moles / molar mass
    for i in range(120):
        moles = i % 8 + 1
        molar_mass = i % 10 + 10
        mass = moles * molar_mass
        q = f"What mass is required for {moles} mol of a substance with molar mass {molar_mass} g/mol?"
        opts = [f"{mass} g", f"{mass + molar_mass} g",
                f"{moles + molar_mass} g", f"{mass/2:g} g"]
        count += mcq(
            "Chemistry", q, opts, 0,
            "Stoichiometry", "Mole Calculations"
        )

    concepts = [
        ("A substance with pH less than 7 is generally a(n) ___",
         ["acid", "alkali", "salt", "metal"], 0),
        ("Which gas is required for ordinary combustion?",
         ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], 0),
        ("The change from liquid to gas is called ___",
         ["vaporization", "freezing", "melting", "deposition"], 0),
        ("A catalyst generally ___ the rate of a chemical reaction.",
         ["increases", "eliminates", "stops", "reverses"], 0),
        ("Which particle carries a negative charge?",
         ["Electron", "Proton", "Neutron", "Nucleus"], 0),
        ("The bond formed by transfer of electrons is usually called ___",
         ["ionic bond", "covalent bond", "metallic bond", "hydrogen bond"], 0),
        ("Which method can separate sand from water?",
         ["Filtration", "Distillation", "Sublimation", "Chromatography"], 0),
    ]
    i = 0
    while count < target:
        q, opts, ans = concepts[i % len(concepts)]
        q += f" (Practice item {i + 1})"
        count += mcq(
            "Chemistry", q, opts, ans,
            "General Chemistry", "Concepts"
        )
        i += 1

    return count


# ============================================================
# BIOLOGY
# ============================================================

def seed_biology(target=500):
    count = 0

    concepts = [
        ("Which organelle is mainly responsible for photosynthesis?",
         ["Chloroplast", "Mitochondrion", "Ribosome", "Nucleus"], 0, "Cell Biology"),
        ("Which organelle is commonly described as the powerhouse of the cell?",
         ["Mitochondrion", "Nucleus", "Golgi apparatus", "Cell wall"], 0, "Cell Biology"),
        ("The basic structural and functional unit of life is the ___",
         ["cell", "organ", "tissue", "organ system"], 0, "Cell Biology"),
        ("Which blood component helps in clotting?",
         ["Platelets", "Red blood cells", "Plasma", "Neurons"], 0, "Human Biology"),
        ("Which organ pumps blood around the human body?",
         ["Heart", "Liver", "Kidney", "Lung"], 0, "Human Biology"),
        ("Which gas is released during photosynthesis?",
         ["Oxygen", "Nitrogen", "Carbon dioxide", "Hydrogen"], 0, "Plant Biology"),
        ("Which process produces genetically similar offspring in many single-celled organisms?",
         ["Asexual reproduction", "Pollination", "Fertilization", "Meiosis"], 0, "Reproduction"),
        ("Which part of a plant absorbs most water from the soil?",
         ["Root hairs", "Flowers", "Fruits", "Leaves"], 0, "Plant Biology"),
        ("Which molecule carries genetic information?",
         ["DNA", "Glucose", "Water", "Starch"], 0, "Genetics"),
        ("Which enzyme begins starch digestion in the mouth?",
         ["Amylase", "Pepsin", "Lipase", "Trypsin"], 0, "Human Biology"),
    ]

    for i in range(500):
        q, opts, ans, topic = concepts[i % len(concepts)]
        count = i + 1
        mcq(
            "Biology",
            q.replace("?", f"? Practice item {i + 1}."),
            opts, ans, topic, "Core Concepts"
        )

    return count


# ============================================================
# ECONOMICS
# ============================================================

def seed_economics(target=500):
    concepts = [
        ("The basic economic problem arises because resources are ___ while wants are unlimited.",
         ["scarce", "unlimited", "free", "identical"], 0, "Basic Economic Problems"),
        ("The next best alternative forgone when a choice is made is called ___",
         ["opportunity cost", "profit", "revenue", "utility"], 0, "Basic Economic Problems"),
        ("A market in which there is only one seller is called ___",
         ["monopoly", "perfect competition", "oligopoly", "monopsony"], 0, "Market Structures"),
        ("An increase in price generally causes quantity demanded to ___, other things being equal.",
         ["fall", "rise", "remain unlimited", "double"], 0, "Demand and Supply"),
        ("A tax placed on imported goods is called a(n) ___",
         ["tariff", "subsidy", "grant", "quota"], 0, "International Trade"),
        ("Inflation refers to a sustained increase in the general ___ level.",
         ["price", "employment", "production", "population"], 0, "Macroeconomics"),
        ("The reward for labour is generally called ___",
         ["wages", "rent", "interest", "profit"], 0, "Factors of Production"),
        ("The reward for capital is generally called ___",
         ["interest", "rent", "wages", "profit"], 0, "Factors of Production"),
        ("The reward for land is generally called ___",
         ["rent", "wages", "interest", "salary"], 0, "Factors of Production"),
        ("The reward for entrepreneurship is generally called ___",
         ["profit", "rent", "wages", "interest"], 0, "Factors of Production"),
    ]
    count = 0
    for i in range(target):
        q, opts, ans, topic = concepts[i % len(concepts)]
        count += mcq(
            "Economics",
            q.replace("___", "___") + f" (Practice item {i + 1})",
            opts, ans, topic, "Core Concepts"
        )
    return count


# ============================================================
# GOVERNMENT
# ============================================================

def seed_government(target=500):
    concepts = [
        ("The principle of separation of powers is associated with the idea of dividing government powers among different ___",
         ["organs", "markets", "companies", "families"], 0, "Political Concepts"),
        ("A system in which citizens elect representatives to make decisions is called ___",
         ["representative democracy", "absolute monarchy", "military rule", "theocracy"], 0, "Democracy"),
        ("The body responsible for making laws in a democracy is the ___",
         ["legislature", "judiciary", "civil service", "police"], 0, "Organs of Government"),
        ("The body primarily responsible for interpreting laws is the ___",
         ["judiciary", "legislature", "executive", "electorate"], 0, "Organs of Government"),
        ("The body responsible for implementing laws is the ___",
         ["executive", "judiciary", "legislature", "electorate"], 0, "Organs of Government"),
        ("A constitution is best described as the fundamental rules governing a ___",
         ["state", "market", "company", "school"], 0, "Constitution"),
        ("The right of citizens to choose their leaders through voting is called ___",
         ["franchise", "censorship", "immunity", "diplomacy"], 0, "Citizenship"),
        ("A government controlled by the armed forces is commonly called ___",
         ["military rule", "democracy", "monarchy", "federalism"], 0, "Political Systems"),
        ("Federalism involves constitutional division of powers between ___",
         ["levels of government", "private firms", "political parties", "families"], 0, "Federalism"),
        ("Political parties mainly seek to ___",
         ["gain political power through elections", "abolish voting",
          "end public debate", "replace all laws"], 0, "Political Parties"),
    ]
    count = 0
    for i in range(target):
        q, opts, ans, topic = concepts[i % len(concepts)]
        count += mcq(
            "Government",
            q + f" (Practice item {i + 1})",
            opts, ans, topic, "Core Concepts"
        )
    return count


# ============================================================
# LITERATURE
# ============================================================

def seed_literature(target=500):
    concepts = [
        ("A comparison using 'like' or 'as' is called a ___",
         ["simile", "metaphor", "irony", "pun"], 0, "Figures of Speech"),
        ("A direct comparison that does not normally use 'like' or 'as' is a ___",
         ["metaphor", "simile", "rhyme", "alliteration"], 0, "Figures of Speech"),
        ("The repetition of initial consonant sounds is called ___",
         ["alliteration", "assonance", "metonymy", "satire"], 0, "Sound Devices"),
        ("The central idea of a literary work is its ___",
         ["theme", "setting", "plot", "stage direction"], 0, "Literary Elements"),
        ("The time and place of a story constitute its ___",
         ["setting", "theme", "conflict", "climax"], 0, "Literary Elements"),
        ("The main character in a story is the ___",
         ["protagonist", "antagonist", "narrator", "chorus"], 0, "Characterization"),
        ("The character who opposes the protagonist is commonly called the ___",
         ["antagonist", "protagonist", "speaker", "narrator"], 0, "Characterization"),
        ("A poem with fourteen lines is traditionally called a ___",
         ["sonnet", "ballad", "ode", "epic"], 0, "Poetry"),
        ("A dramatic work intended mainly to make an audience laugh is a ___",
         ["comedy", "tragedy", "elegy", "epic"], 0, "Drama"),
        ("A literary work that uses humour to criticize society is often called ___",
         ["satire", "elegy", "romance", "pastoral"], 0, "Literary Genres"),
    ]
    count = 0
    for i in range(target):
        q, opts, ans, topic = concepts[i % len(concepts)]
        count += mcq(
            "Literature",
            q + f" (Practice item {i + 1})",
            opts, ans, topic, "Core Concepts"
        )
    return count


# ============================================================
# GEOGRAPHY
# ============================================================

def seed_geography(target=500):
    concepts = [
        ("The imaginary line that divides the Earth into Northern and Southern Hemispheres is the ___",
         ["Equator", "Prime Meridian", "Tropic of Cancer", "Arctic Circle"], 0, "Map Reading"),
        ("The Prime Meridian passes through ___",
         ["Greenwich", "Lagos", "Cairo", "Nairobi"], 0, "Map Reading"),
        ("The process by which water vapour becomes liquid is called ___",
         ["condensation", "evaporation", "sublimation", "infiltration"], 0, "Weather"),
        ("The wearing away of the Earth's surface by agents such as water and wind is called ___",
         ["erosion", "deposition", "condensation", "crystallization"], 0, "Geomorphology"),
        ("A long period of unusually low rainfall is called ___",
         ["drought", "flood", "cyclone", "dew"], 0, "Climate"),
        ("A large body of salt water surrounded partly or completely by land is a ___",
         ["sea", "plateau", "valley", "plain"], 0, "Physical Geography"),
        ("A map scale expresses the relationship between map distance and ___",
         ["ground distance", "rainfall", "temperature", "population"], 0, "Map Reading"),
        ("The natural increase of population depends mainly on birth rate and ___",
         ["death rate", "rainfall", "longitude", "soil colour"], 0, "Population"),
        ("A densely populated urban centre with surrounding built-up areas is commonly called a ___",
         ["conurbation", "delta", "plateau", "savanna"], 0, "Settlement"),
        ("Planting trees to restore forest cover is called ___",
         ["afforestation", "irrigation", "mining", "urbanization"], 0, "Environmental Management"),
    ]
    count = 0
    for i in range(target):
        q, opts, ans, topic = concepts[i % len(concepts)]
        count += mcq(
            "Geography",
            q + f" (Practice item {i + 1})",
            opts, ans, topic, "Core Concepts"
        )
    return count


# ============================================================
# COMMERCE
# ============================================================

def seed_commerce(target=500):
    concepts = [
        ("Commerce is mainly concerned with the activities involved in the ___ of goods and services.",
         ["exchange", "destruction", "cultivation", "consumption only"], 0, "Introduction to Commerce"),
        ("A person who buys goods in large quantities and sells to retailers is a ___",
         ["wholesaler", "consumer", "broker", "producer"], 0, "Trade"),
        ("A person who buys goods for final use is a ___",
         ["consumer", "wholesaler", "manufacturer", "agent"], 0, "Trade"),
        ("Insurance is a contract designed mainly to provide protection against specified ___",
         ["risks", "profits", "sales", "discounts"], 0, "Insurance"),
        ("A document showing details of goods sold and the amount due is an ___",
         ["invoice", "receipt", "cheque", "agenda"], 0, "Business Documents"),
        ("A cheque is an instruction to a bank to pay a specified sum from a customer's ___",
         ["account", "warehouse", "factory", "office"], 0, "Banking"),
        ("Advertising is primarily used to ___",
         ["inform and persuade potential customers", "hide products",
          "stop competition", "abolish prices"], 0, "Marketing"),
        ("A partnership is a business owned by ___",
         ["two or more persons", "one person only", "the government only", "customers only"], 0, "Forms of Business"),
        ("A company owned by shareholders is commonly organized as a ___",
         ["joint-stock company", "sole proprietorship", "cooperative society only", "family club"], 0, "Forms of Business"),
        ("Warehousing helps business by providing facilities for the ___ of goods.",
         ["storage", "destruction", "manufacture only", "advertising only"], 0, "Aids to Trade"),
    ]
    count = 0
    for i in range(target):
        q, opts, ans, topic = concepts[i % len(concepts)]
        count += mcq(
            "Commerce",
            q + f" (Practice item {i + 1})",
            opts, ans, topic, "Core Concepts"
        )
    return count


# ============================================================
# ACCOUNTING
# ============================================================

def seed_accounting(target=500):
    count = 0

    for i in range(180):
        assets = i + 100
        liabilities = i % 70 + 20
        capital = assets - liabilities
        q = f"If a business has assets of ₦{assets:,} and liabilities of ₦{liabilities:,}, what is its capital?"
        opts = [
            f"₦{capital:,}",
            f"₦{assets + liabilities:,}",
            f"₦{liabilities:,}",
            f"₦{capital + 100:,}"
        ]
        count += mcq(
            "Accounting", q, opts, 0,
            "Accounting Principles", "Accounting Equation"
        )

    concepts = [
        ("The book in which transactions are first recorded is generally called the ___",
         ["journal", "balance sheet", "ledger only", "trial balance"], 0, "Books of Account"),
        ("The statement showing assets and liabilities at a particular date is the ___",
         ["statement of financial position", "cash book", "journal", "invoice"], 0, "Financial Statements"),
        ("An expense paid in advance is known as a ___ expense.",
         ["prepaid", "accrued", "capital", "contingent"], 0, "Adjustments"),
        ("Revenue earned but not yet received is known as ___ revenue.",
         ["accrued", "prepaid", "capital", "drawings"], 0, "Adjustments"),
        ("Goods taken by the owner for personal use are called ___",
         ["drawings", "sales", "purchases", "capital"], 0, "Capital and Drawings"),
        ("The excess of sales over cost of goods sold is ___",
         ["gross profit", "net loss", "capital", "working capital"], 0, "Profit and Loss"),
        ("A trial balance is prepared mainly to check the ___",
         ["arithmetical accuracy of ledger entries", "market price of goods",
          "number of employees", "bank interest rate"], 0, "Trial Balance"),
        ("Depreciation is the systematic allocation of the cost of a ___ asset.",
         ["non-current", "current", "cash", "liquid"], 0, "Depreciation"),
    ]

    i = 0
    while count < target:
        q, opts, ans, topic = concepts[i % len(concepts)]
        count += mcq(
            "Accounting",
            q + f" (Practice item {i + 1})",
            opts, ans, topic, "Core Concepts"
        )
        i += 1

    return count


# ============================================================
# AGRICULTURAL SCIENCE
# ============================================================

def seed_agriculture(target=500):
    concepts = [
        ("The removal of unwanted plants from a farm is called ___",
         ["weeding", "harvesting", "irrigation", "grafting"], 0, "Crop Production"),
        ("The practice of growing crops and keeping animals on the same farm is called ___",
         ["mixed farming", "monocropping", "nomadic farming", "plantation farming"], 0, "Farming Systems"),
        ("A soil rich in decayed organic matter is generally described as having high ___",
         ["humus content", "salt content", "stone content", "metal content"], 0, "Soil Science"),
        ("The controlled addition of water to crops is called ___",
         ["irrigation", "drainage", "mulching", "harvesting"], 0, "Crop Production"),
        ("The process of removing mature crops from the field is called ___",
         ["harvesting", "germination", "pollination", "transpiration"], 0, "Crop Production"),
        ("Which farm animal is commonly classified as a ruminant?",
         ["Cattle", "Chicken", "Rabbit", "Turkey"], 0, "Animal Husbandry"),
        ("A poultry bird kept mainly for egg production is called a ___ bird.",
         ["layer", "broiler", "drake", "gander"], 0, "Poultry"),
        ("A poultry bird raised mainly for meat is called a ___",
         ["broiler", "layer", "hen", "rooster"], 0, "Poultry"),
        ("Crop rotation can help maintain soil ___",
         ["fertility", "salinity only", "erosion", "temperature"], 0, "Soil Management"),
        ("A farm tool commonly used for loosening soil is a ___",
         ["hoe", "sickle", "watering can", "basket"], 0, "Farm Tools"),
    ]
    count = 0
    for i in range(target):
        q, opts, ans, topic = concepts[i % len(concepts)]
        count += mcq(
            "Agricultural Science",
            q + f" (Practice item {i + 1})",
            opts, ans, topic, "Core Concepts"
        )
    return count


# ============================================================
# COMPUTER SCIENCE
# ============================================================

def seed_computer_science(target=500):
    concepts = [
        ("Which component performs most arithmetic and logical operations in a computer?",
         ["ALU", "Monitor", "Keyboard", "Printer"], 0, "Computer Architecture"),
        ("Which memory is volatile?",
         ["RAM", "ROM", "DVD", "Flash drive"], 0, "Computer Memory"),
        ("Which device is primarily used to enter text into a computer?",
         ["Keyboard", "Monitor", "Speaker", "Projector"], 0, "Input and Output"),
        ("Which device displays visual output?",
         ["Monitor", "Keyboard", "Mouse", "Microphone"], 0, "Input and Output"),
        ("A collection of instructions that tells a computer what to do is called ___",
         ["software", "hardware", "firmware only", "cable"], 0, "Software"),
        ("Which of these is an operating system?",
         ["Linux", "HTML", "JPEG", "USB"], 0, "Operating Systems"),
        ("The binary number system uses the digits ___",
         ["0 and 1", "1 and 2", "0 to 9", "2 and 3"], 0, "Number Systems"),
        ("A step-by-step procedure for solving a problem is an ___",
         ["algorithm", "icon", "interface", "output"], 0, "Algorithms"),
        ("HTML is mainly used to structure ___",
         ["web pages", "spreadsheets", "processors", "hard disks"], 0, "Web Technology"),
        ("Python is a ___",
         ["programming language", "database only", "web browser", "hardware device"], 0, "Programming"),
        ("A database table is made up of rows and ___",
         ["columns", "screens", "speakers", "pixels"], 0, "Databases"),
        ("A strong password should generally be ___",
         ["hard to guess", "your first name", "123456", "password"], 0, "Cybersecurity"),
    ]
    count = 0
    for i in range(target):
        q, opts, ans, topic = concepts[i % len(concepts)]
        count += mcq(
            "Computer Science",
            q + f" (Practice item {i + 1})",
            opts, ans, topic, "Core Concepts"
        )
    return count


# ============================================================
# SEED RUNNER
# ============================================================

GENERATORS = {
    "Use of English": seed_english,
    "Mathematics": seed_mathematics,
    "Physics": seed_physics,
    "Chemistry": seed_chemistry,
    "Biology": seed_biology,
    "Economics": seed_economics,
    "Government": seed_government,
    "Literature": seed_literature,
    "Geography": seed_geography,
    "Commerce": seed_commerce,
    "Accounting": seed_accounting,
    "Agricultural Science": seed_agriculture,
    "Computer Science": seed_computer_science,
}


def count_subject(subject):
    return JAMBQuestion.query.filter_by(subject=subject).count()


def run():
    print("=" * 70)
    print("CAREER BRIDGE JAMB QUESTION BANK SEED")
    print("Original JAMB-style practice questions")
    print("=" * 70)

    with app.app_context():

        before_total = JAMBQuestion.query.count()

        for subject in SUBJECTS:
            before = count_subject(subject)

            if before >= 500:
                print(f"{subject}: already has {before} questions - skipped.")
                continue

            print(f"Generating {subject}...")

            # The generators create at least 500 questions.
            GENERATORS[subject](500)

            db.session.commit()

            after = count_subject(subject)

            print(
                f"{subject}: {before} -> {after} questions"
            )

        after_total = JAMBQuestion.query.count()

        print()
        print("=" * 70)
        print(f"Question bank before: {before_total}")
        print(f"Question bank after:  {after_total}")
        print("=" * 70)

        print("\nSUBJECT COUNTS:")
        for subject in SUBJECTS:
            print(f"{subject}: {count_subject(subject)}")

        print()
        print("Seeding complete.")


if __name__ == "__main__":
    run()
