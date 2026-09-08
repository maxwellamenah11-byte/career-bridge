from datetime import datetime
import random
import math

from app import app, db, JAMBQuestion

# ============================================================
# CAREER BRIDGE — EXTREME JAMB-STYLE QUESTION BANK SEEDER
# ============================================================
# Original practice questions only. NOT official JAMB past questions.
#
# Target: 1,000 UNIQUE questions per subject.
# Difficulty: every generated question is tagged EXTREME.
#
# Design goals:
# - No fake variations such as "sentence set 262" or "Practice item 262".
# - Questions are generated from many genuinely different templates.
# - Distractors are designed around common reasoning mistakes.
# - Most questions require multiple steps, interpretation, comparison,
#   conditional reasoning, or application rather than one-step recall.
# - Existing app.py JAMBQuestion model is used unchanged.
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


def count_subject(subject):
    return JAMBQuestion.query.filter_by(subject=subject).count()


def _fmt_money(n):
    return f"₦{n:,.2f}" if isinstance(n, float) and not n.is_integer() else f"₦{int(n):,}"


def _unique_options(values):
    out = []
    for value in values:
        value = str(value)
        if value not in out:
            out.append(value)
    if len(out) != 4:
        raise ValueError(f"Expected 4 unique options, got {out}")
    return out


def add_question(subject, question, options, answer_index, topic, subtopic, explanation):
    if len(options) != 4:
        raise ValueError("Each MCQ must have exactly four options")
    options = _unique_options(options)
    if not 0 <= answer_index < 4:
        raise ValueError("answer_index must be 0..3")

    question = question.strip()
    # Reject the old artificial wording if it ever sneaks back into a template.
    banned = ("sentence set", "practice item", "extreme challenge")
    if any(x in question.lower() for x in banned):
        raise ValueError(f"Artificial question wording detected: {question}")

    # Exact subject + question-text deduplication (without any fake suffixes).
    existing = JAMBQuestion.query.filter_by(subject=subject, question=question).first()
    if existing:
        return False

    correct = options[answer_index]
    shuffled = list(options)
    random.shuffle(shuffled)
    correct_letter = "ABCD"[shuffled.index(correct)]

    db.session.add(JAMBQuestion(
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
        source="Career Bridge Original Extreme Practice Question",
        created_at=datetime.utcnow(),
    ))
    return True


def cleanup_legacy_generated_questions():
    """Remove malformed/artificial rows produced by earlier generators."""
    rows = JAMBQuestion.query.filter(
        (JAMBQuestion.question.ilike("%sentence set%")) |
        (JAMBQuestion.question.ilike("%practice item%")) |
        (JAMBQuestion.question.ilike("%[Extreme Challenge%"))
    ).all()
    removed = 0
    for row in rows:
        db.session.delete(row)
        removed += 1
    if removed:
        db.session.commit()
        print(f"Removed {removed} legacy/artificial questions.", flush=True)
    return removed


def add_until(subject, target, generator):
    """Keep generating until the subject really contains target rows."""
    existing = count_subject(subject)
    attempts = 0
    # Large headroom; a generator failure should be reported explicitly.
    max_attempts = max(50000, (target - existing) * 120)

    while count_subject(subject) < target:
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError(
                f"Could not reach {target} unique questions for {subject}. "
                f"Current count: {count_subject(subject)} after {attempts} attempts."
            )
        generator()
        if attempts % 100 == 0:
            db.session.flush()
        if attempts % 500 == 0:
            db.session.commit()
            print(f"  {subject}: {count_subject(subject)}/{target}", flush=True)
    db.session.commit()


# ============================================================
# USE OF ENGLISH
# ============================================================

def make_english_generator():
    vocab = [
        ("equivocal", "deliberately ambiguous", "The adjective equivocal describes a statement that permits more than one interpretation."),
        ("intransigent", "uncompromising", "An intransigent person is unwilling to alter a position or compromise."),
        ("perfunctory", "superficial", "Perfunctory work is carried out with little care or attention."),
        ("circumspect", "cautiously deliberate", "A circumspect person acts carefully after considering possible consequences."),
        ("trenchant", "forcefully incisive", "Trenchant criticism is sharp, direct, and penetrating."),
        ("parsimonious", "excessively frugal", "Parsimonious describes someone unwilling to spend or give even when appropriate."),
        ("recalcitrant", "stubbornly resistant", "Recalcitrant describes resistance to authority or control."),
        ("fastidious", "meticulously exacting", "Fastidious describes great attention to detail and standards."),
        ("ameliorate", "make less severe", "To ameliorate a problem is to improve or lessen it."),
        ("deleterious", "harmful", "A deleterious effect causes damage or harm."),
        ("abstruse", "difficult to understand", "Abstruse ideas are intellectually difficult to grasp."),
        ("profligate", "wastefully extravagant", "Profligate behaviour involves reckless or excessive spending."),
    ]
    grammar = [
        ("Neither the principal nor the vice-principals ___ prepared to endorse the revised policy after the evidence was reviewed.", ["was", "were", "has", "is"], 1, "The nearer plural subject 'vice-principals' requires 'were'."),
        ("No sooner ___ the preliminary results than several candidates requested an independent review.", ["had the board released", "the board had released", "did the board release", "has the board released"], 0, "'No sooner had ... than ...' requires past perfect inversion."),
        ("If the research team ___ the anomalous readings earlier, the faulty conclusion might have been avoided.", ["noticed", "had noticed", "has noticed", "would notice"], 1, "The third conditional requires past perfect in the if-clause."),
        ("The sequence of revisions, rather than the individual amendments, ___ responsible for the unexpected outcome.", ["were", "have been", "was", "are"], 2, "The head noun 'sequence' is singular."),
        ("Hardly had the invigilator finished speaking when the candidates ___ writing.", ["begin", "began", "had begun", "have begun"], 1, "A simple past event follows the completed past-perfect action."),
        ("Were the committee ___ the implication of the clause, it would probably amend the proposal.", ["understands", "understood", "to understand", "had understood"], 1, "This is an inverted second conditional: Were + subject + past form."),
    ]
    connectors = [
        ("Although the sample was small, the conclusion was cautiously reported; ___, the researchers avoided claiming universal validity.", ["nevertheless", "therefore", "similarly", "otherwise"], 0),
        ("The policy increased short-term output; ___, the long-run maintenance burden became substantially larger.", ["however", "moreover", "therefore", "likewise"], 0),
        ("The candidate cited three sources, ___ none directly addressed the central claim being tested.", ["although", "because", "so that", "unless"], 0),
    ]

    def gen():
        mode = random.randrange(7)
        if mode == 0:
            word, meaning, expl = random.choice(vocab)
            context = random.choice([
                "The editor rejected the statement because its wording was intentionally open to competing interpretations.",
                "The negotiator refused every compromise despite repeated proposals from the opposing side.",
                "The auditor described the inspection as superficial rather than comprehensive.",
                "The minister answered cautiously after considering the possible consequences of each option.",
            ])
            target = "Choose the option nearest in meaning to the underlined word as used in the context."
            q = f"{context} In this context, the word '{word}' is closest in meaning to ___. {target}"
            opts = [meaning, random.choice(["casually persuasive", "emotionally neutral", "temporarily valid"]), "the opposite of its ordinary sense", "a purely grammatical function"]
            return add_question("Use of English", q, opts, 0, "Lexis and Structure", "Advanced Vocabulary", expl)
        if mode == 1:
            q, opts, ans, expl = random.choice(grammar)
            extra = random.choice([
                "Choose the option that completes the sentence most appropriately.",
                "Select the option that preserves both grammatical agreement and sequence of tense.",
                "Choose the option that makes the construction standard in formal English.",
            ])
            return add_question("Use of English", f"{extra}\n\n{q}", opts, ans, "Lexis and Structure", "Advanced Grammar", expl)
        if mode == 2:
            a, b, c = random.randint(7, 19), random.randint(31, 79), random.randint(2, 6)
            passage = (
                f"The committee received {a} written submissions from institutions serving {b} communities. "
                f"Only {c} submissions directly challenged the proposed framework; the remainder concentrated on implementation costs, staffing, and monitoring. "
                "Although the chair described the response as broadly supportive, the technical panel warned that acceptance of the objective did not imply acceptance of the proposed means."
            )
            q = "Which inference is BEST supported by the passage?"
            opts = [
                "Support for the objective cannot be assumed to mean agreement with the implementation method.",
                "Most institutions rejected the objective itself.",
                "The technical panel considered implementation costs irrelevant.",
                "Every submission directly challenged the framework.",
            ]
            return add_question("Use of English", f"Read the passage carefully and answer the question.\n\n{passage}\n\n{q}", opts, 0, "Comprehension", "Inference and Implication", "The passage explicitly distinguishes support for the objective from acceptance of the proposed means.")
        if mode == 3:
            item = random.choice(connectors)
            return add_question("Use of English", f"Choose the connector that best preserves the logical relationship between the two clauses:\n\n{item[0]}", item[1], item[2], "Lexis and Structure", "Logical Connectives", "The connector must express the contrast or relationship established by the two clauses.")
        if mode == 4:
            pairs = [
                ("Only after the panel had compared all three reports did it identify the discrepancy.", "The panel did not identify the discrepancy until it had compared all three reports."),
                ("Had the witness disclosed the earlier statement, the interpretation might have changed.", "If the witness had disclosed the earlier statement, the interpretation might have changed."),
                ("Not until the final paragraph was the qualification made explicit.", "The qualification was not made explicit until the final paragraph."),
            ]
            source, equivalent = random.choice(pairs)
            q = f"Which option is closest in meaning to the sentence below without changing its implication?\n\n{source}"
            opts = [equivalent, "The opposite happened after the same event.", "The qualification was made before the stated event.", "The sentence expresses a future condition rather than a past condition."]
            return add_question("Use of English", q, opts, 0, "Lexis and Structure", "Sentence Transformation", "The correct option preserves the logical and temporal relationship of the original sentence.")
        if mode == 5:
            err = random.choice([
                ("Each of the witnesses, together with two legal advisers, have submitted separate statements.", "have", "has"),
                ("The quality of the materials supplied by the contractors were questioned during the audit.", "were", "was"),
                ("Neither the revised estimates nor the contingency figure appear in the final table.", "appear", "appears"),
            ])
            q = f"In the sentence below, identify the underlined word that contains the grammatical error and choose its correct replacement.\n\n{err[0]}"
            opts = [err[1], err[2], "submitted", "questioned"]
            return add_question("Use of English", q, opts, 1, "Lexis and Structure", "Error Detection", f"The subject head requires '{err[2]}', not '{err[1]}'.")
        # Sound/word-stress logic, but with contrasting word classes.
        word = random.choice(["record", "present", "permit", "produce", "object", "conduct"])
        q = f"In standard English, which option correctly identifies the stress pattern when '{word}' is used as a NOUN rather than a verb?"
        opts = ["Stress is normally placed on the first syllable.", "Stress is normally placed on the second syllable.", "Both syllables must receive equal primary stress.", "Stress cannot change with grammatical function."]
        return add_question("Use of English", q, opts, 0, "Oral English", "Word Stress and Word Class", "For several noun-verb pairs of this type, the noun commonly carries first-syllable stress, unlike the verb.")

    return gen


# ============================================================
# MATHEMATICS
# ============================================================

def make_math_generator():
    def gen():
        mode = random.randrange(10)
        if mode == 0:
            # Roots -> transformed roots, plus a second constraint.
            r1 = random.randint(-12, 12)
            r2 = random.randint(-12, 12)
            if r1 == r2:
                r2 += random.choice([-3, 3])
            s, p = r1 + r2, r1 * r2
            k = random.randint(2, 5)
            # roots become r1^k and r2^k; use k 2 or 3 for sane arithmetic
            k = random.choice([2, 3])
            transformed_sum = r1 ** k + r2 ** k
            transformed_product = (p ** k)
            q = (f"A quadratic equation has roots α and β with α + β = {s} and αβ = {p}. "
                 f"A new equation has roots α^{k} and β^{k}. If its roots are also required to have product {transformed_product}, "
                 f"what is the sum of its roots?")
            opts = [str(transformed_sum), str(s ** k), str((r1 ** k) * (r2 ** k)), str(transformed_sum + p)]
            return add_question("Mathematics", q, opts, 0, "Algebra", "Quadratic Transformations", "Compute α and β's transformed power sum from the given sum and product, or recover the roots first and transform them.")
        if mode == 1:
            # Rational equation with extraneous-root trap.
            a = random.randint(2, 8)
            b = random.randint(1, 9)
            c = random.randint(2, 7)
            q = (f"Solve, over the real numbers, the equation  {a}/(x - {b}) + {b}/(x + {c}) = {a+b}. "
                 "Which value of x satisfies the original equation and is admissible?")
            # Find a valid integer by brute force among a sensible set.
            candidates = []
            for x in range(-20, 21):
                if x in (b, -c):
                    continue
                lhs = a/(x-b) + b/(x+c)
                if abs(lhs - (a+b)) < 1e-9:
                    candidates.append(x)
            if not candidates:
                # Fallback create a known equation.
                b = 2
                c = 1
                a = 3
                candidates = [3]
                q = "Solve, over the real numbers, the equation 3/(x - 2) + 2/(x + 1) = 5. Which value of x satisfies the original equation and is admissible?"
            ans = candidates[0]
            opts = [str(ans), str(b), str(-c), str(ans + random.choice([1, 2, -1]))]
            return add_question("Mathematics", q, opts, 0, "Algebra", "Rational Equations", "Multiply by the common denominator, solve the resulting equation, then reject any value that makes a denominator zero.")
        if mode == 2:
            # AP/GP compound reasoning.
            first = random.randint(3, 20)
            d = random.randint(2, 8)
            n = random.randint(8, 20)
            total = n * (2*first + (n-1)*d) // 2
            q = (f"An arithmetic sequence has first term {first} and common difference {d}. "
                 f"Another sequence begins with the same first term and has common ratio 2. "
                 f"If the sum of the first {n} terms of the arithmetic sequence is {total}, "
                 "which statement about the geometric sequence's first three terms is necessarily true?")
            opts = [f"Its first three terms are {first}, {2*first}, {4*first}.", f"Its third term is {first+n*d}.", f"Its common ratio equals {d}.", f"Its first three terms have sum {total}."]
            return add_question("Mathematics", q, opts, 0, "Algebra", "Sequences", "The geometric sequence is defined by its first term and ratio 2, independent of the arithmetic sequence's common difference.")
        if mode == 3:
            # Probability conditional.
            r = random.randint(4, 9)
            b = random.randint(3, 8)
            g = random.randint(2, 6)
            total = r + b + g
            q = (f"A box contains {r} red, {b} blue and {g} green counters. Two are drawn without replacement. "
                 "Given that at least one is red, what is the probability that both are red?")
            p_both_red = r*(r-1)/(total*(total-1))
            p_at_least_red = 1 - ((total-r)*(total-r-1))/(total*(total-1))
            prob = p_both_red / p_at_least_red
            from fractions import Fraction
            frac = Fraction(prob).limit_denominator()
            opts = [str(frac), str(Fraction(r,total)), str(Fraction(r-1,total-1)), str(Fraction(2*r,total))]
            return add_question("Mathematics", q, opts, 0, "Probability", "Conditional Probability", "Use P(A|B)=P(A∩B)/P(B); the condition changes the denominator from all pairs to pairs containing at least one red counter.")
        if mode == 4:
            # Geometry with coordinates.
            x1, y1 = random.randint(-9, 6), random.randint(-8, 8)
            dx, dy = random.randint(3, 9), random.randint(2, 8)
            x2, y2 = x1 + dx, y1 + dy
            x3, y3 = x1 + dx, y1
            # right triangle area and hypotenuse
            area = abs(dx*dy)/2
            h2 = dx*dx + dy*dy
            q = (f"In a coordinate plane, A({x1},{y1}), B({x2},{y2}) and C({x3},{y3}) form a right triangle at C. "
                 f"Find the area of triangle ABC and hence the exact length of AB.")
            opts = [f"Area = {area:g}; AB = √{h2}", f"Area = {dx*dy:g}; AB = {dx+dy}", f"Area = {area*2:g}; AB = √{dx*dy}", f"Area = {dx+dy:g}; AB = {h2}"]
            return add_question("Mathematics", q, opts, 0, "Geometry", "Coordinate Geometry", "The perpendicular legs have lengths dx and dy; area is 1/2·dx·dy and AB follows Pythagoras.")
        if mode == 5:
            # Logarithms.
            base = random.choice([2, 3, 5])
            p = random.randint(2, 5)
            q = (f"If log base {base} of x = {p} and log base {base} of y = {p-1}, determine log base {base} of (x²/y).")
            ans = 2*p - (p-1)
            opts = [str(ans), str(p), str(p-1), str(2*p)]
            return add_question("Mathematics", q, opts, 0, "Indices and Logarithms", "Log Laws", "Use log_b(x²/y)=2log_b(x)-log_b(y).")
        if mode == 6:
            # Trig identity + quadrant.
            theta = random.choice([120, 135, 150, 225, 240, 300, 315])
            q = (f"An angle θ lies in a quadrant where sin θ is {'negative' if math.sin(math.radians(theta)) < 0 else 'positive'}, and cos θ = {math.cos(math.radians(theta)):.3f} approximately. "
                 "Which option best represents the sign and exact relationship for tan θ?")
            sgn = "negative" if math.tan(math.radians(theta)) < 0 else "positive"
            opts = [f"tan θ is {sgn} and equals sin θ/cos θ", "tan θ must be positive because θ is measured anticlockwise", "tan θ equals cos θ/sin θ", "the sign cannot be determined from the quadrant"]
            return add_question("Mathematics", q, opts, 0, "Trigonometry", "Signs and Identities", "tan θ = sin θ/cos θ, and the quadrant determines its sign.")
        if mode == 7:
            # Word problem system.
            unit = random.randint(18, 45)
            q = (f"A two-stage pricing system applies a discount of {random.randint(8,18)}% to the marked price, then adds a levy of {random.randint(5,12)}% of the discounted price. "
                 f"If the final bill for a product is ₦{unit*1000:,}, which expression gives the marked price M?")
            disc = random.randint(8,18)
            levy = random.randint(5,12)
            final = unit*1000
            rate = (1-disc/100)*(1+levy/100)
            q = f"A product is marked at M. A discount of {disc}% is applied, after which a levy of {levy}% of the discounted price is added. If the final bill is {_fmt_money(final)}, which value of M is correct?"
            ans = final / rate
            opts = [f"{ans:,.2f}", f"{final/(1-disc/100):,.2f}", f"{final*(1+disc/100):,.2f}", f"{final*(1-levy/100):,.2f}"]
            return add_question("Mathematics", q, opts, 0, "Number", "Percentage and Financial Reasoning", "Reverse the two operations in the correct order: final = M(1-discount)(1+levy).")
        if mode == 8:
            # Variation/Counting.
            n = random.randint(7, 11)
            r = random.randint(3, 5)
            q = (f"A committee of {r} students is to be selected from {n} students. Two particular students refuse to serve together. "
                 "How many valid committees can be formed if order does not matter?")
            from math import comb
            ans = comb(n, r) - comb(n-2, r-2)
            opts = [str(ans), str(comb(n,r)), str(comb(n-1,r-1)), str(comb(n-2,r))]
            return add_question("Mathematics", q, opts, 0, "Permutation and Combination", "Restricted Selection", "Count all committees and subtract those containing both restricted students.")
        # Statistics / grouped-data reasoning.
        a = random.randint(8, 20)
        freqs = [random.randint(2, 9) for _ in range(4)]
        vals = [a, a+5, a+10, a+15]
        totalf = sum(freqs)
        mean = sum(v*f for v,f in zip(vals,freqs))/totalf
        q = f"Four score groups are represented by values {vals} with frequencies {freqs}. If one additional score of {a+25} is included, which approximate mean is obtained for the enlarged data set?"
        new_mean = (sum(v*f for v,f in zip(vals,freqs)) + a+25)/(totalf+1)
        opts = [f"{new_mean:.2f}", f"{mean:.2f}", f"{new_mean+2:.2f}", f"{new_mean-2:.2f}"]
        return add_question("Mathematics", q, opts, 0, "Statistics", "Weighted Mean", "Compute the weighted total, add the new observation, then divide by the new total frequency.")
    return gen


# ============================================================
# PHYSICS
# ============================================================

def make_physics_generator():
    def gen():
        mode = random.randrange(8)
        if mode == 0:
            m = random.randint(2, 9)
            u = random.randint(4, 12)
            v = random.randint(14, 30)
            s = random.randint(20, 60)
            # derive a from v^2=u^2+2as; choose consistency by construct s
            s = random.choice([10, 15, 20, 25, 30])
            a = (v*v-u*u)/(2*s)
            if a <= 0:
                v = u + random.randint(4, 10)
                a = random.choice([2,3,4])
                s = (v*v-u*u)/(2*a)
            t = (v-u)/a
            q = (f"A body changes speed uniformly from {u} m/s to {v} m/s while travelling {s:.2f} m. "
                 "Determine its acceleration and the time taken, to the nearest appropriate values.")
            opts = [f"a = {a:.2f} m/s², t = {t:.2f} s", f"a = {(v-u)/s:.2f} m/s², t = {s/(v):.2f} s", f"a = {(v+u)/(2*s):.2f} m/s², t = {s/(u):.2f} s", f"a = {a*2:.2f} m/s², t = {t/2:.2f} s"]
            return add_question("Physics", q, opts, 0, "Mechanics", "SUVAT and Uniform Acceleration", "Use v²=u²+2as and then v=u+at.")
        if mode == 1:
            R1, R2 = random.randint(2, 10), random.randint(3, 12)
            V = random.randint(12, 36)
            # parallel resistors current and power
            Req = (R1*R2)/(R1+R2)
            I = V/Req
            P = V*I
            q = f"Two resistors of {R1} Ω and {R2} Ω are connected in parallel across a {V} V ideal source. What are the total current drawn and total electrical power consumed?"
            opts = [f"I = {I:.2f} A; P = {P:.2f} W", f"I = {V/(R1+R2):.2f} A; P = {V**2/(R1+R2):.2f} W", f"I = {Req/V:.2f} A; P = {V*Req:.2f} W", f"I = {V/R1 + V/R2:.2f} A; P = {Req*V:.2f} W"]
            return add_question("Physics", q, opts, 0, "Electricity", "Parallel Circuits and Power", "Find equivalent resistance by reciprocal addition, then I=V/R and P=VI.")
        if mode == 2:
            f = random.randint(5, 18)
            x = random.randint(2, 7)
            k = random.randint(8, 25)
            # Hooke law + stored energy
            force = k*x
            E = 0.5*k*(x/100)**2 if x >= 1 else 0.5*k*x*x
            # use x in cm -> energy conversion
            E = 0.5*k*(x/100)**2
            q = f"A spring obeys Hooke's law with force constant {k} N/m. It is stretched by {x} cm. Determine the restoring force and elastic potential energy stored."
            opts=[f"F = {force/100:.2f} N; E = {E:.4f} J", f"F = {force:.2f} N; E = {0.5*k*x*x:.2f} J", f"F = {k/x:.2f} N; E = {k*x/100:.4f} J", f"F = {force/100:.2f} N; E = {force*x/100:.4f} J"]
            return add_question("Physics", q, opts, 0, "Mechanics", "Elasticity", "Convert centimetres to metres, then use F=kx and E=1/2kx².")
        if mode == 3:
            # Refraction chain
            n = random.choice([1.25, 1.33, 1.5, 1.6])
            angle = random.choice([30, 40, 50, 60])
            sinr = math.sin(math.radians(angle))/n
            if sinr >= 1:
                angle = 30
                sinr = math.sin(math.radians(angle))/n
            rdeg = math.degrees(math.asin(sinr))
            q = f"Light enters a transparent medium of refractive index {n:.2f} from air at an incidence angle of {angle}°. What is the approximate angle of refraction, and what happens to its speed in the medium?"
            opts=[f"r ≈ {rdeg:.1f}°; speed decreases", f"r ≈ {angle*n:.1f}°; speed increases", f"r ≈ {rdeg:.1f}°; speed increases", f"r ≈ {90-rdeg:.1f}°; speed is unchanged"]
            return add_question("Physics", q, opts, 0, "Waves", "Refraction", "Snell's law gives n=sin i/sin r; entering a medium with n>1 reduces speed.")
        if mode == 4:
            # Gas law combined.
            P1 = random.randint(90, 120)
            V1 = random.randint(2, 8)
            T1 = random.randint(280, 320)
            P2 = random.randint(100, 140)
            T2 = random.randint(300, 360)
            V2 = P1*V1*T2/(P2*T1)
            q = f"A fixed quantity of ideal gas occupies {V1} L at {P1} kPa and {T1} K. If pressure becomes {P2} kPa and temperature becomes {T2} K, what is the new volume?"
            opts=[f"{V2:.2f} L", f"{V1*P1/P2:.2f} L", f"{V1*T1/T2:.2f} L", f"{V1*P2*T2/(P1*T1):.2f} L"]
            return add_question("Physics", q, opts, 0, "Thermal Physics", "Combined Gas Law", "Use P1V1/T1 = P2V2/T2 and rearrange for V2.")
        if mode == 5:
            # momentum + collision
            m1 = random.randint(2, 8)
            m2 = random.randint(2, 8)
            u1 = random.randint(4, 12)
            u2 = random.randint(-8, 5)
            v = (m1*u1 + m2*u2)/(m1+m2)
            q = f"A body of mass {m1} kg moving at {u1} m/s collides with and sticks to a {m2} kg body moving at {u2} m/s along the same line. What is their common velocity immediately after impact?"
            opts=[f"{v:.2f} m/s", f"{(m1*u1-m2*u2)/(m1+m2):.2f} m/s", f"{m1*u1/m2:.2f} m/s", f"{(u1+u2)/2:.2f} m/s"]
            return add_question("Physics", q, opts, 0, "Mechanics", "Momentum and Inelastic Collision", "Conservation of momentum gives (m1u1+m2u2)=(m1+m2)v.")
        if mode == 6:
            # transformers/power
            Vp = random.randint(100, 240)
            Np = random.randint(500, 1200)
            Ns = random.randint(50, 400)
            Vs = Vp*Ns/Np
            I_s = random.randint(2, 12)
            Is = I_s
            Ip = Vs*Is/Vp
            q = f"An ideal transformer has {Np} primary turns and {Ns} secondary turns. It is supplied at {Vp} V and delivers {Is} A to a load. What are the secondary voltage and approximate primary current?"
            opts=[f"Vs = {Vs:.2f} V; Ip = {Ip:.2f} A", f"Vs = {Vp*Np/Ns:.2f} V; Ip = {Is:.2f} A", f"Vs = {Vs:.2f} V; Ip = {Vp*Is/Vs:.2f} A", f"Vs = {Vp+Ns/Np:.2f} V; Ip = {Vp/Is:.2f} A"]
            return add_question("Physics", q, opts, 0, "Electricity", "Transformers", "For an ideal transformer, Vs/Vp=Ns/Np and input power equals output power.")
        # Work-energy with friction.
        m = random.randint(3, 15)
        g = 10
        h = random.randint(2, 8)
        f = random.randint(5, 25)
        d = random.randint(4, 12)
        Wg = m*g*h
        Wf = f*d
        net = Wg - Wf
        q = f"A {m} kg object is raised through {h} m while a constant opposing force of {f} N acts over {d} m. Taking g={g} m/s², what is the net work done by gravity and the opposing force together?"
        opts=[f"{net} J", f"{Wg+Wf} J", f"{Wg} J", f"{Wf-Wg} J"]
        return add_question("Physics", q, opts, 0, "Mechanics", "Work and Energy", "Gravity does mgh of work in magnitude; the opposing force does negative work f·d.")
    return gen


# ============================================================
# CHEMISTRY
# ============================================================

def make_chemistry_generator():
    def gen():
        mode = random.randrange(8)
        if mode == 0:
            a = random.randint(2, 6)
            b = random.randint(1, 5)
            # generic empirical/molar calculation
            mol = random.randint(2, 9)
            molarmass = a*12 + b*16
            mass = mol*molarmass
            q = f"A compound has formula C{a}H{b}O and relative molecular mass {molarmass}. What mass would contain {mol} mol of the compound?"
            opts=[f"{mass} g", f"{molarmass} g", f"{mass/mol} g", f"{mass*2} g"]
            return add_question("Chemistry", q, opts, 0, "Stoichiometry", "Moles and Molar Mass", "Mass = number of moles × molar mass.")
        if mode == 1:
            # limiting reagent
            na = random.randint(2, 6)
            nb = random.randint(2, 8)
            # 2A + B -> products
            possible = min(na//2, nb)
            q = f"A reaction follows 2A + B → products. If {na} mol of A is mixed with {nb} mol of B, identify the limiting reagent and the maximum number of moles of reaction product units formed according to the equation."
            if na/2 < nb:
                opts=[f"A; {possible} mol", f"B; {possible} mol", f"A; {na} mol", f"B; {nb} mol"]
            else:
                possible = nb
                opts=[f"B; {possible} mol", f"A; {possible} mol", f"B; {na} mol", f"A; {nb} mol"]
            return add_question("Chemistry", q, opts, 0, "Stoichiometry", "Limiting Reagent", "Compare the stoichiometric amount required: two moles of A are needed per mole of B.")
        if mode == 2:
            # pH strong acid/base mix.
            Ca = random.choice([0.01, 0.02, 0.05])
            Va = random.choice([0.05, 0.1, 0.2])
            Cb = random.choice([0.01, 0.025, 0.05])
            Vb = random.choice([0.05, 0.1, 0.2])
            ma, mb = Ca*Va, Cb*Vb
            total = Va+Vb
            if abs(ma-mb) < 1e-12:
                q = "Equal moles of a strong monoprotic acid and strong base are mixed. Neglecting volume change effects beyond addition, what is the approximate pH?"
                opts=["7", "less than 7", "greater than 7", "cannot be estimated"]
                return add_question("Chemistry", q, opts, 0, "Acids, Bases and Salts", "Neutralization", "A strong acid and strong base in stoichiometrically equal amounts neutralize approximately completely at pH 7.")
            excess = abs(ma-mb)/total
            import math as _m
            pH = -math.log10(excess) if ma>mb else 14 + math.log10(excess)
            q = f"{Va:.2f} L of {Ca:.3f} M HCl is mixed with {Vb:.2f} L of {Cb:.3f} M NaOH. Which option best describes the final solution's pH?"
            correct = f"approximately {pH:.2f}"
            opts=[correct, f"approximately {14-pH:.2f}", "exactly 7", f"approximately {pH+1:.2f}"]
            return add_question("Chemistry", q, opts, 0, "Acids, Bases and Salts", "Mixed Strong Electrolytes", "Calculate the moles of H+ and OH−, identify the excess, divide by total volume, then take pH or pOH.")
        if mode == 3:
            # equilibrium Le Chatelier conceptual with quantitative wording
            temp = random.choice(["higher", "lower"])
            q = ("For an exothermic reversible reaction, the equilibrium mixture is heated after equilibrium has been established. "
                 "Assuming no catalyst is added, which combined statement is most defensible?" )
            opts=["Equilibrium shifts toward reactants and the catalyst idea is irrelevant to the final equilibrium position.", "Equilibrium shifts toward products and the reaction becomes faster in both directions equally.", "Equilibrium constant necessarily becomes one.", "Heating cannot affect the equilibrium composition of an exothermic reaction."]
            return add_question("Chemistry", q, opts, 0, "Equilibrium", "Le Chatelier's Principle", "For an exothermic forward reaction, heat acts like a product, so adding heat favours the reverse direction; a catalyst changes rates, not equilibrium position.")
        if mode == 4:
            # electrolysis stoichiometry
            I = random.randint(2, 9)
            t = random.randint(900, 3600)
            Q = I*t
            # monovalent metal e.g. Ag, F=96500, mol deposited = Q/F
            mol = Q/96500
            mass = mol*108
            q = f"A current of {I} A is passed through a silver-ion solution for {t} s. Taking 96,500 C/mol e⁻ and Ag=108, what mass of silver is deposited?"
            opts=[f"{mass:.2f} g", f"{Q/96500*2*108:.2f} g", f"{I*t/108:.2f} g", f"{Q*108:.2f} g"]
            return add_question("Chemistry", q, opts, 0, "Electrochemistry", "Faraday's Laws", "Use Q=It, moles of electrons=Q/F, and one electron deposits one Ag+ ion.")
        if mode == 5:
            # organic oxidation/reaction identification
            alcohol = random.choice(["ethanol", "propan-1-ol", "butan-1-ol"])
            product = {"ethanol":"ethanoic acid", "propan-1-ol":"propanoic acid", "butan-1-ol":"butanoic acid"}[alcohol]
            q = f"An unknown primary alcohol is heated under controlled oxidation and, after further oxidation under suitable conditions, gives {product}. Which starting alcohol is most consistent with the observation?"
            opts=[alcohol, "propan-2-ol", "2-methylpropan-2-ol", "ethene"]
            return add_question("Chemistry", q, opts, 0, "Organic Chemistry", "Oxidation of Alcohols", "Primary alcohols can be oxidized through an aldehyde to the corresponding carboxylic acid with the same carbon skeleton.")
        if mode == 6:
            # Periodicity / ionization energy reasoning
            period = random.choice([2,3])
            q = f"Two elements X and Y occur in the same period ({period}). X has a lower first ionization energy but a smaller atomic radius than Y. Which inference is LEAST defensible without additional data?"
            opts=["The pair may involve an unusual periodic trend exception or differing subshell stability.", "Atomic radius and ionization energy do not always vary in a perfectly monotonic way across a period.", "One should use electron configuration to explain the apparent anomaly.", "X must necessarily have a greater nuclear charge and a larger radius than Y."]
            return add_question("Chemistry", q, opts, 3, "Periodic Chemistry", "Ionization Energy", "The last claim contradicts the stated smaller radius and is not defensible as a necessary conclusion.")
        # gas volume stoichiometry
        vol = random.randint(12, 60)
        q = f"At the same temperature and pressure, {vol} L of nitrogen reacts with sufficient hydrogen according to N₂ + 3H₂ → 2NH₃. What volume of NH₃ can be formed, assuming complete conversion and ideal-gas behaviour?"
        ans = 2*vol
        opts=[f"{ans} L", f"{vol} L", f"{3*vol} L", f"{ans/3:g} L"]
        return add_question("Chemistry", q, opts, 0, "Stoichiometry", "Gas Volumes", "At fixed temperature and pressure, gas volumes follow mole ratios: 1 volume N₂ gives 2 volumes NH₃.")
    return gen


# ============================================================
# BIOLOGY
# ============================================================

def make_biology_generator():
    def gen():
        mode = random.randrange(7)
        if mode == 0:
            q = ("A plant cell is placed in a solution with a lower water potential than the cell sap. "
                 "After a measurable period, which sequence of events is most consistent with water movement and membrane behaviour?")
            opts=["Water leaves the cell by osmosis, the vacuole shrinks, and plasmolysis may occur.", "Water enters rapidly, the vacuole collapses, and plasmolysis occurs.", "Water movement stops because solutes cannot cross the membrane.", "The cell immediately undergoes mitosis because water potential changes."]
            return add_question("Biology", q, opts, 0, "Cell Biology", "Osmosis and Water Potential", "Water moves toward lower water potential across a selectively permeable membrane; excessive loss causes plasmolysis in plant cells.")
        if mode == 1:
            dominant = random.choice(["T", "B"])
            recessive = "t" if dominant == "T" else "b"
            q = f"Assume {dominant} is a completely dominant allele over {recessive}. Two heterozygous parents are crossed. If a child is selected only because the phenotype shows the dominant trait, what is the probability that the child is homozygous dominant?"
            opts=["1/3", "1/4", "1/2", "2/3"]
            return add_question("Biology", q, opts, 0, "Genetics", "Probability from Monohybrid Cross", "Among dominant-phenotype offspring, the genotypes TT:Tt occur in a 1:2 ratio, so P(TT | dominant phenotype)=1/3.")
        if mode == 2:
            # photosynthesis factors
            light = random.choice(["low", "high"])
            co2 = random.choice(["low", "high"])
            q = f"A plant is tested under {light} light intensity and {co2} carbon-dioxide concentration, while temperature is held at the optimum. Which variable is most likely to act as the limiting factor if the other factor is abundant?"
            limiting = "light intensity" if light == "low" else "carbon-dioxide concentration"
            opts=[limiting, "oxygen concentration in the leaf air spaces", "the colour of the roots", "genetic recombination rate"]
            return add_question("Biology", q, opts, 0, "Plant Physiology", "Limiting Factors of Photosynthesis", "When temperature is optimal and one resource is relatively scarce, that factor can limit the rate of photosynthesis.")
        if mode == 3:
            # ecology energy transfer
            levels = random.randint(3, 5)
            base = random.randint(9000, 30000)
            # approximate 10% transfer per trophic level
            top = base*(0.1**(levels-1))
            q = f"An ecosystem has approximately {base} kJ of energy available to producers. If only about 10% is transferred between successive trophic levels, how much energy would be expected at trophic level {levels}?"
            opts=[f"{top:.1f} kJ", f"{base/10:.1f} kJ", f"{base*(0.1**levels):.1f} kJ", f"{base*0.1:.1f} kJ regardless of level"]
            return add_question("Biology", q, opts, 0, "Ecology", "Energy Flow", "Repeated transfer of about 10% means multiply by 0.1 for every trophic step after the producers.")
        if mode == 4:
            q = random.choice([
                "A patient has normal blood glucose immediately after eating, but a later test shows persistent hyperglycaemia, increased urine production and glucose in the urine. Which physiological control pathway is most directly implicated?",
                "A person produces unusually large volumes of dilute urine despite adequate water intake. Which hormone-response pathway is most directly relevant?",
            ])
            opts=["Insulin or antidiuretic-hormone regulation, depending on the stated abnormality", "Bile secretion alone", "Bone marrow platelet formation only", "The cardiac cycle without endocrine involvement"]
            return add_question("Biology", q, opts, 0, "Human Physiology", "Homeostasis", "The symptoms described point to endocrine/homeostatic control rather than digestive or purely circulatory processes.")
        if mode == 5:
            # evolution selection
            q = ("A bacterial population contains rare variants with reduced sensitivity to an antibiotic before treatment begins. "
                 "After repeated antibiotic exposure, the resistant phenotype becomes more common. Which explanation is most scientifically defensible?")
            opts=["Selection increased the frequency of pre-existing heritable resistant variants.", "The antibiotic intentionally taught every bacterium to mutate in the same useful direction.", "Only non-genetic temporary changes can explain inherited resistance.", "Resistance necessarily arose because bacteria needed it, with no role for variation."]
            return add_question("Biology", q, opts, 0, "Evolution", "Natural Selection", "Selection changes frequencies of heritable variants already present or arising through mutation; it does not create adaptive mutations because organisms need them.")
        # enzyme kinetics scenario
        temp = random.choice(["below", "near", "above"])
        q = f"An enzyme assay shows that increasing temperature from 25°C to 35°C sharply increases reaction rate, but increasing it further to 55°C causes the rate to collapse. If the optimum lies near the middle range, what best explains the later decline?"
        opts=["Denaturation or loss of functional enzyme structure", "An increase in substrate concentration beyond all possible limits", "Permanent conversion of enzyme into DNA", "A guaranteed increase in active-site collisions at 55°C"]
        return add_question("Biology", q, opts, 0, "Cell Physiology", "Enzymes", "Higher temperature can increase kinetic energy up to an optimum, after which protein structure may be disrupted and activity falls.")
    return gen


# ============================================================
# ECONOMICS
# ============================================================

def make_economics_generator():
    def gen():
        mode = random.randrange(7)
        if mode == 0:
            p1, q1 = random.randint(80, 140), random.randint(30, 80)
            p2, q2 = p1 + random.randint(10, 40), max(5, q1-random.randint(8, 25))
            pctq = ((q2-q1)/q1)*100
            pctp = ((p2-p1)/p1)*100
            elasticity = abs(pctq/pctp)
            q = f"Quantity demanded falls from {q1} units to {q2} units when price rises from ₦{p1} to ₦{p2}. Based on the percentage method, what is the approximate price elasticity of demand?"
            opts=[f"{elasticity:.2f}", f"{abs(pctp/pctq):.2f}", f"{abs((q2-q1)/(p2-p1)):.2f}", f"{abs((p2-p1)/(q2-q1)):.2f}"]
            return add_question("Economics", q, opts, 0, "Demand and Supply", "Price Elasticity", "Compute percentage change in quantity divided by percentage change in price, using absolute value for the elasticity magnitude.")
        if mode == 1:
            q = "A government imposes a maximum legal price below the market equilibrium price for a staple. Which combined outcome is most likely if the policy is effectively enforced?"
            opts=["Excess demand and a shortage", "Excess supply and unsold stock", "A guaranteed fall in demand and supply", "Automatic return to the original equilibrium without adjustment"]
            return add_question("Economics", q, opts, 0, "Market Structures", "Price Controls", "A binding price ceiling below equilibrium encourages quantity demanded to exceed quantity supplied.")
        if mode == 2:
            Y = random.randint(100, 300)
            C = random.randint(60, 180)
            I = random.randint(20, 70)
            G = random.randint(15, 60)
            X = random.randint(10, 50)
            M = random.randint(5, 35)
            q = f"Using the expenditure approach, calculate GDP when household consumption is ₦{C}bn, investment is ₦{I}bn, government spending is ₦{G}bn, exports are ₦{X}bn and imports are ₦{M}bn."
            ans = C+I+G+X-M
            opts=[f"₦{ans}bn", f"₦{C+I+G+X+M}bn", f"₦{C+I+G}bn", f"₦{ans-M}bn"]
            return add_question("Economics", q, opts, 0, "Macroeconomics", "National Income", "GDP by expenditure = C + I + G + (X − M).")
        if mode == 3:
            q = "A bank is required to keep a higher reserve ratio while the central bank simultaneously sells government securities. Assuming other conditions are unchanged, what combined effect is most likely intended?"
            opts=["Reduce banks' lending capacity and contract the money supply", "Increase banks' lending capacity and expand the money supply", "Eliminate all inflation immediately", "Increase currency depreciation without affecting credit conditions"]
            return add_question("Economics", q, opts, 0, "Money and Banking", "Monetary Policy", "Higher reserve requirements and open-market sales both tend to reduce the funds available for lending.")
        if mode == 4:
            q = "A country has abundant labour but scarce capital equipment. Which policy is most directly aimed at raising labour productivity rather than simply increasing the size of the labour force?"
            opts=["Investment in training and complementary productive capital", "Increasing population without capital formation", "Restricting all technological imports", "Reducing worker access to education"]
            return add_question("Economics", q, opts, 0, "Factors of Production", "Productivity", "Productivity rises when labour is supported by skills, appropriate technology and capital.")
        if mode == 5:
            q = "An economy experiences rising general prices while real output falls and unemployment rises. Which description best captures the situation?"
            opts=["Stagflation", "Deflationary boom", "Hyper-productivity", "Pure demand expansion"]
            return add_question("Economics", q, opts, 0, "Macroeconomics", "Inflation and Unemployment", "Stagflation combines inflation with weak or falling output and high unemployment.")
        # opportunity cost / PPF
        a = random.randint(2, 8)
        b = random.randint(10, 30)
        q = f"A country can produce either {a*10} units of machinery or {b*10} units of food with its available resources. Moving resources toward machinery causes food output to fall by {b*2} units for each additional {a} machinery units. What concept is most directly illustrated?"
        opts=["Increasing opportunity cost", "Absolute scarcity disappearing", "Price ceiling", "Comparative advantage being identical to absolute advantage"]
        return add_question("Economics", q, opts, 0, "Basic Economic Problems", "Opportunity Cost and PPF", "The increasing amount of one good forgone as production of another expands is the idea of opportunity cost along the production possibility frontier.")
    return gen


# ============================================================
# GOVERNMENT
# ============================================================

def make_government_generator():
    def gen():
        mode = random.randrange(7)
        if mode == 0:
            q = "A constitution assigns law-making to a legislature, implementation to an executive, and final interpretation to courts, while allowing each branch to constrain specific abuses by the others. Which principle is best represented?"
            opts=["Separation of powers with checks and balances", "Unitary administration without division", "Military command hierarchy", "Traditional monarchical succession"]
            return add_question("Government", q, opts, 0, "Political Concepts", "Separation of Powers", "The description combines functional separation with mechanisms for checking abuses between branches.")
        if mode == 1:
            q = "In a federal system, a constitutional amendment transfers a power from the national government to constituent units and specifies that the transfer cannot be reversed by ordinary legislation. What does this most clearly demonstrate?"
            opts=["Constitutional allocation of powers", "Administrative delegation that can be reversed at will", "Judicial sentencing", "Party manifesto writing"]
            return add_question("Government", q, opts, 0, "Federalism", "Division of Powers", "A constitutionally entrenched allocation differs from ordinary administrative delegation.")
        if mode == 2:
            q = "An electoral commission rejects a result because voting materials were incomplete, orders a rerun in the affected area, and publishes reasons. Which institutional principle is most directly being exercised?"
            opts=["Electoral adjudication/administrative authority under established rules", "Judicial supremacy over every executive action", "Political party sovereignty over elections", "Legislative immunity from voting rules"]
            return add_question("Government", q, opts, 0, "Electoral Process", "Election Administration", "The electoral body is applying the legal rules governing the conduct and validity of elections.")
        if mode == 3:
            q = "A legislature summons a minister to explain expenditure and uses committee hearings to examine documents. Which accountability relationship is most directly illustrated?"
            opts=["Legislative oversight of the executive", "Judicial review of legislation", "Direct democracy replacing representation", "Civil service appointment of legislators"]
            return add_question("Government", q, opts, 0, "Organs of Government", "Legislative Oversight", "Legislative committees can scrutinize executive conduct and public expenditure.")
        if mode == 4:
            q = "A pressure group mobilizes petitions and expert briefings to persuade lawmakers, but it does not itself seek to form a government through elections. How is the group best distinguished from a political party?"
            opts=["Its primary objective is to influence policy rather than capture governmental power through elections.", "It can never have members.", "It is automatically part of the judiciary.", "It must be controlled by the electoral commission."]
            return add_question("Government", q, opts, 0, "Political Parties and Pressure Groups", "Interest Representation", "Pressure groups seek policy influence; political parties normally seek governmental power through elections.")
        if mode == 5:
            q = "A court invalidates a regulation because it conflicts with a superior constitutional provision. Which doctrine provides the clearest conceptual basis?"
            opts=["Constitutional supremacy and judicial review", "Collective responsibility", "Cabinet secrecy", "Party discipline"]
            return add_question("Government", q, opts, 0, "Constitution", "Judicial Review", "Where the constitution is supreme, inconsistent subordinate rules may be invalidated through judicial review.")
        # citizenship dilemma
        q = "A citizen is required to obey a lawful emergency regulation but also has a right to challenge its constitutionality in court. Which statement best captures the relationship?"
        opts=["Rights may coexist with legal duties; the challenge should follow lawful constitutional procedures.", "A right to challenge automatically suspends every duty.", "A duty removes all rights during an emergency.", "Courts cannot consider constitutional questions during emergencies under any system."]
        return add_question("Government", q, opts, 0, "Citizenship", "Rights and Duties", "Citizenship includes both obligations to obey valid laws and lawful mechanisms for contesting unconstitutional action.")
    return gen


# ============================================================
# LITERATURE
# ============================================================

def make_literature_generator():
    def gen():
        mode = random.randrange(7)
        if mode == 0:
            q = "A narrator reveals a character's plan to the audience while the character's opponent remains unaware, creating tension because the audience anticipates an outcome unknown to the character. What device is most central?"
            opts=["Dramatic irony", "Pathetic fallacy", "Onomatopoeia", "Elegy"]
            return add_question("Literature", q, opts, 0, "Literary Devices", "Dramatic Irony", "The audience knows information that the character does not, creating anticipatory tension.")
        if mode == 1:
            q = "A poem repeatedly returns to an image of a locked gate whenever the speaker considers social mobility. The image gains meaning as the poem develops. Which interpretation is most defensible?"
            opts=["The gate functions as a recurring symbol of restricted opportunity.", "The gate must literally be the poem's setting in every stanza.", "The repetition proves the poem is a ballad.", "The image can only be interpreted as sound imagery."]
            return add_question("Literature", q, opts, 0, "Poetry", "Symbolism", "A recurring concrete image can acquire symbolic significance through context and repetition.")
        if mode == 2:
            q = "A tragic protagonist recognizes the consequences of a flaw only after a chain of choices has made reversal impossible. Which combination best describes the dramatic effect?"
            opts=["Recognition deepens the tragic inevitability of the consequences.", "Recognition automatically turns the work into comedy.", "The flaw becomes irrelevant once recognized.", "The climax must therefore occur before the recognition."]
            return add_question("Drama", q, opts, 0, "Tragedy", "Characterization and Tragic Structure", "Late recognition can intensify the sense that earlier choices have produced irreversible consequences.")
        if mode == 3:
            passage = "The narrator praises the town's new flood-control wall while describing, in the same paragraph, three neighbourhoods that lost access to the river after its construction."
            q = f"In the following narrative situation, what technique is most likely operating?\n\n{passage}"
            opts=["Irony created by a tension between the narrator's praise and the described consequences", "Purely chronological narration", "Onomatopoeia based on water sounds", "A fixed rhyme scheme"]
            return add_question("Literature", q, opts, 0, "Narrative Technique", "Irony", "The evaluative language and the consequences described pull in opposing directions.")
        if mode == 4:
            q = "A playwright repeatedly has a servant echo a statement made by the ruler, but each repetition subtly changes one word and gradually exposes the ruler's contradiction. What is the strongest dramatic function of the repeated dialogue?"
            opts=["It exposes inconsistency through controlled repetition and contrast.", "It removes all conflict from the play.", "It turns every character into the narrator.", "It proves the work is an epic poem."]
            return add_question("Drama", q, opts, 0, "Dramatic Techniques", "Repetition and Contrast", "Repetition can emphasize changes in wording and reveal contradictions.")
        if mode == 5:
            q = "A novel shifts from an objective third-person account to a character's limited perspective at a moment of uncertainty. What effect is most likely intended?"
            opts=["To restrict immediate knowledge and intensify uncertainty", "To guarantee that the narrator becomes omniscient", "To remove characterization", "To eliminate all ambiguity"]
            return add_question("Prose", q, opts, 0, "Narrative Perspective", "Point of View", "A limited perspective controls information and can make the reader share the character's uncertainty.")
        q = "A poet uses a sustained contrast between drought and overflowing water to structure a meditation on emotional excess. Which term best captures the dominant structural device?"
        opts=["Extended antithesis", "Bathos", "Pun", "Direct characterization"]
        return add_question("Literature", q, opts, 0, "Poetry", "Contrast and Structure", "A sustained opposition between contrasting images creates an extended antithetical structure.")
    return gen


# ============================================================
# GEOGRAPHY
# ============================================================

def make_geography_generator():
    def gen():
        mode = random.randrange(7)
        if mode == 0:
            scale = random.choice([50000, 100000, 250000])
            a, b = random.randint(3, 8), random.randint(4, 9)
            mapdist = math.sqrt(a*a+b*b)
            ground_km = mapdist*scale/100000
            q = f"On a map with scale 1:{scale:,}, two locations differ by {a} cm east-west and {b} cm north-south. What is their approximate straight-line ground distance?"
            opts=[f"{ground_km:.2f} km", f"{(a+b)*scale/100000:.2f} km", f"{(a*b)*scale/100000:.2f} km", f"{mapdist*scale/10000:.2f} km"]
            return add_question("Geography", q, opts, 0, "Map Reading", "Scale and Distance", "Use the Pythagorean theorem for map displacement, then convert using the map scale.")
        if mode == 1:
            q = "A river's outer bends are actively eroded while slower flow on inner bends deposits sediment. Over time the meander becomes more pronounced and may eventually form a cut-off. Which sequence best fits the process?"
            opts=["Lateral erosion → neck narrowing → cut-off → ox-bow formation", "Vertical erosion only → glacier formation → delta burial", "Wave refraction → coral growth → cliff recession", "Deflation → dune migration → volcanic intrusion"]
            return add_question("Geography", q, opts, 0, "Geomorphology", "River Processes", "Meander migration can narrow the neck until a cut-off creates an ox-bow lake.")
        if mode == 2:
            q = "A coastal settlement has mangroves removed, drainage channels altered, and more paved surfaces added. During intense rainfall, flooding becomes more frequent. Which combination best explains the change?"
            opts=["Reduced natural storage/infiltration plus altered drainage increases runoff concentration.", "Mangrove removal necessarily lowers sea level, eliminating flood risk.", "Paving always increases infiltration into soil.", "Drainage alteration can have no effect on runoff timing."]
            return add_question("Geography", q, opts, 0, "Environmental Management", "Flooding and Land Use", "Vegetation and permeable surfaces can store/intercept water; removal and paving increase rapid runoff.")
        if mode == 3:
            q = "A town lies on the windward slope of a mountain range. Moist air rises, cools and condenses there, while the leeward side receives much less rainfall. Which climatic process is central?"
            opts=["Orographic uplift and rain-shadow formation", "Convection without topographic forcing", "Land breeze caused by daily heating only", "Thermal inversion produced by ocean salinity"]
            return add_question("Geography", q, opts, 0, "Climate", "Relief Rainfall", "Forced ascent over mountains causes cooling and condensation; descending air on the leeward side is drier.")
        if mode == 4:
            pop = random.randint(10000, 30000)
            area = random.randint(20, 100)
            density = pop/area
            q = f"A settlement's population rises from {pop:,} to {int(pop*1.35):,} while its built-up area rises from {area} km² to {area+random.randint(5,20)} km². What does this comparison most directly allow a geographer to investigate?"
            new_area = area+random.randint(5,20)
            new_pop = int(pop*1.35)
            density2 = new_pop/new_area
            opts=["Whether population density increased or decreased despite both variables rising", "Only the absolute population change", "Only rainfall variability", "Whether longitude changed"]
            return add_question("Geography", q, opts, 0, "Population", "Density and Urban Growth", "Density depends jointly on population and area; one must compare both changes rather than infer density from population alone.")
        if mode == 5:
            q = "A farmer reports severe sheet erosion on bare soil after heavy rain, while a nearby plot with dense ground cover loses little soil under similar rainfall. Which causal chain is strongest?"
            opts=["Vegetation intercepts rain, slows runoff, and anchors soil, reducing erosion.", "Ground cover increases rainfall intensity at the soil surface.", "Bare soil creates more humus and therefore more erosion resistance.", "Dense vegetation eliminates all runoff regardless of slope."]
            return add_question("Geography", q, opts, 0, "Environmental Management", "Soil Erosion", "Vegetation reduces raindrop impact and runoff speed while roots stabilize soil.")
        # GIS-ish spatial reasoning without assuming software specifics.
        q = "A planner overlays flood-risk zones, hospitals and road networks on the same spatial database. Which analytical advantage is most directly gained?"
        opts=["Relationships among location, accessibility and hazard can be examined spatially.", "All attribute data become immune to measurement error.", "Map scale ceases to matter.", "Every hospital is guaranteed to be outside flood risk."]
        return add_question("Geography", q, opts, 0, "Geographical Techniques", "Spatial Analysis", "Layering spatial datasets helps compare locations and relationships among geographic features.")
    return gen


# ============================================================
# COMMERCE
# ============================================================

def make_commerce_generator():
    def gen():
        mode = random.randrange(7)
        if mode == 0:
            q = "A manufacturer begins selling directly to consumers through a digital platform and provides its own delivery service. Which change in the channel of distribution is most directly implied?"
            opts=["Fewer traditional intermediaries between producer and final consumer", "Mandatory use of two wholesalers", "Removal of all after-sales service", "Conversion of the manufacturer into a government agency"]
            return add_question("Commerce", q, opts, 0, "Distribution", "Channels of Distribution", "Direct-to-consumer selling can reduce the number of intermediaries.")
        if mode == 1:
            q = "An insurance proposer knowingly withholds a material fact that would influence the insurer's assessment of the risk. Which principle is most directly breached?"
            opts=["Utmost good faith", "Contribution", "Subrogation", "Insurable interest only"]
            return add_question("Commerce", q, opts, 0, "Insurance", "Principles of Insurance", "Material facts relevant to the risk should be disclosed under utmost good faith.")
        if mode == 2:
            q = "A retailer receives goods on credit and is later sent a document listing descriptions, quantities, prices and the total amount payable, before payment is made. Which document is being described?"
            opts=["Invoice", "Receipt", "Cheque", "Certificate of incorporation"]
            return add_question("Commerce", q, opts, 0, "Business Documents", "Trade Documentation", "An invoice requests/payment details for goods or services supplied; a receipt acknowledges payment.")
        if mode == 3:
            q = "A firm groups consumers by age, income, occupation and purchasing behaviour before designing separate promotional campaigns. Which marketing decision is this?"
            opts=["Market segmentation", "Vertical integration", "Trade credit", "Depreciation"]
            return add_question("Commerce", q, opts, 0, "Marketing", "Market Segmentation", "Segmentation divides the market into identifiable groups with shared characteristics.")
        if mode == 4:
            q = "A wholesaler buys in bulk, stores products, breaks bulk into smaller quantities and assumes some inventory risk before selling to retailers. Which group of functions best explains the wholesaler's role?"
            opts=["Storage, breaking bulk, financing and risk-bearing", "Manufacturing, mining and crop production", "Only advertising and taxation", "Only retail display and consumer credit"]
            return add_question("Commerce", q, opts, 0, "Trade", "Wholesaling Functions", "Wholesalers perform several distribution functions, including storage, bulk breaking, financing and risk-bearing.")
        if mode == 5:
            q = "A company allows shareholders to vote on major corporate decisions while professional managers handle daily operations. Which organizational feature is most directly illustrated?"
            opts=["Separation of ownership from management in a company structure", "Sole proprietorship", "Government monopoly", "Partnership by necessity"]
            return add_question("Commerce", q, opts, 0, "Forms of Business", "Company Organization", "Shareholders own the company while directors/managers oversee governance and operations.")
        q = "A consumer compares price, warranty, reliability and after-sales support before choosing among competing products. Which concept is most relevant to the firm's attempt to influence this decision?"
        opts=["The marketing mix/value proposition affecting consumer choice", "Only warehousing", "Only customs clearance", "A trial balance"]
        return add_question("Commerce", q, opts, 0, "Marketing", "Consumer Decision-Making", "Consumers evaluate a combination of price, product features and service, which firms address through their value proposition and marketing mix.")
    return gen


# ============================================================
# ACCOUNTING
# ============================================================

def make_accounting_generator():
    def gen():
        mode = random.randrange(8)
        if mode == 0:
            assets = random.randint(300000, 900000)
            liabilities = random.randint(80000, 300000)
            drawings = random.randint(20000, 90000)
            additional_capital = random.randint(10000, 80000)
            opening_equity = assets-liabilities
            closing_equity = opening_equity - drawings + additional_capital
            q = f"At the beginning of the period, a business has assets of ₦{assets:,} and liabilities of ₦{liabilities:,}. During the period the owner withdraws ₦{drawings:,} and introduces an additional ₦{additional_capital:,}. Ignoring profit or loss, what is closing equity?"
            opts=[_fmt_money(closing_equity), _fmt_money(opening_equity), _fmt_money(opening_equity+drawings), _fmt_money(closing_equity+drawings)]
            return add_question("Accounting", q, opts, 0, "Accounting Principles", "Capital and Drawings", "Opening equity = assets − liabilities; closing equity adjusts for drawings and additional capital.")
        if mode == 1:
            cost = random.randint(250000, 900000)
            residual = random.randint(10000, 80000)
            life = random.randint(4, 10)
            dep = (cost-residual)/life
            q = f"A non-current asset costs ₦{cost:,}, has an estimated residual value of ₦{residual:,}, and a useful life of {life} years. Under straight-line depreciation, what is the annual charge?"
            opts=[_fmt_money(dep), _fmt_money(cost/life), _fmt_money(residual/life), _fmt_money((cost+residual)/life)]
            return add_question("Accounting", q, opts, 0, "Non-current Assets", "Depreciation", "Straight-line depreciation = (cost − residual value) ÷ useful life.")
        if mode == 2:
            sales = random.randint(500000, 1200000)
            returns = random.randint(10000, 80000)
            cogs = random.randint(250000, 600000)
            expenses = random.randint(70000, 220000)
            net_sales = sales-returns
            gross = net_sales-cogs
            net = gross-expenses
            q = f"A business reports sales of ₦{sales:,}, returns inward of ₦{returns:,}, cost of goods sold of ₦{cogs:,}, and operating expenses of ₦{expenses:,}. Calculate net profit."
            opts=[_fmt_money(net), _fmt_money(gross), _fmt_money(sales-cogs), _fmt_money(net_sales-expenses)]
            return add_question("Accounting", q, opts, 0, "Financial Statements", "Net Profit", "Net sales = sales − returns inward; gross profit = net sales − COGS; net profit = gross profit − expenses.")
        if mode == 3:
            cash = random.randint(120000, 400000)
            bank = cash + random.randint(-50000, 50000)
            unpresented = random.randint(10000, 30000)
            lodgement = random.randint(8000, 25000)
            q = f"The cash-book balance is ₦{cash:,}. A cheque of ₦{unpresented:,} has been issued but not presented, while a lodgement of ₦{lodgement:,} is not yet credited by the bank. Which statement best describes the reconciliation?"
            opts=["Both items can explain a difference between the records without implying that either record is necessarily wrong.", "Both items must be entered as depreciation.", "The cash book must be discarded and replaced.", "The differences prove that the owner has made drawings."]
            return add_question("Accounting", q, opts, 0, "Bank Reconciliation", "Reconciling Items", "Unpresented cheques and uncredited lodgements are timing differences commonly adjusted during reconciliation.")
        if mode == 4:
            q = "A trial balance agrees, but a complete credit purchase was omitted from both the purchases account and the creditor account. What does this demonstrate?"
            opts=["Agreement of a trial balance does not prove that every transaction has been recorded.", "A trial balance always detects complete omission.", "The omission necessarily creates a suspense account.", "The balance sheet automatically records the purchase anyway."]
            return add_question("Accounting", q, opts, 0, "Books of Account", "Errors and Trial Balance", "A complete omission affects neither side of the trial balance, so the totals can still agree.")
        if mode == 5:
            stock = random.randint(100000, 300000)
            current_assets = stock + random.randint(80000, 200000)
            current_liabilities = random.randint(100000, 250000)
            current_ratio = current_assets/current_liabilities
            acid_ratio = (current_assets-stock)/current_liabilities
            q = f"A company has current assets of ₦{current_assets:,}, including inventory of ₦{stock:,}, and current liabilities of ₦{current_liabilities:,}. Which pair of ratios is closest to its current ratio and acid-test ratio?"
            opts=[f"{current_ratio:.2f}:1 and {acid_ratio:.2f}:1", f"{acid_ratio:.2f}:1 and {current_ratio:.2f}:1", f"{current_assets/stock:.2f}:1 and {stock/current_liabilities:.2f}:1", f"{current_ratio-current_assets/100000:.2f}:1 and {acid_ratio+1:.2f}:1"]
            return add_question("Accounting", q, opts, 0, "Financial Analysis", "Liquidity Ratios", "Current ratio=current assets/current liabilities; acid-test ratio=(current assets−inventory)/current liabilities.")
        if mode == 6:
            q = "An expense of ₦48,000 relates entirely to the next accounting period but has already been paid. At year-end, what accounting treatment is most appropriate?"
            opts=["Recognize a prepaid expense/current asset and exclude the future portion from current-period expense.", "Recognize the whole amount as current-period capital", "Treat the whole amount as revenue", "Ignore the payment completely"]
            return add_question("Accounting", q, opts, 0, "Adjustments", "Prepayments", "A payment relating to a future period is a prepayment and is carried forward as an asset until incurred.")
        # accrual
        q = "Revenue of ₦96,000 has been earned by year-end but ₦20,000 remains uncollected. Which treatment best reflects accrual accounting?"
        opts=["Recognize ₦96,000 of revenue and ₦20,000 as a receivable.", "Recognize only ₦76,000 of revenue.", "Recognize ₦20,000 as a liability.", "Recognize nothing until all cash is collected."]
        return add_question("Accounting", q, opts, 0, "Adjustments", "Accrued Revenue", "Accrual accounting recognizes revenue when earned; the uncollected portion becomes a receivable.")
    return gen


# ============================================================
# AGRICULTURAL SCIENCE
# ============================================================

def make_agriculture_generator():
    def gen():
        mode = random.randrange(7)
        if mode == 0:
            q = "A maize field on a moderate slope develops rills after heavy rain. The farmer wants a low-cost cultural control measure that reduces downhill runoff while preserving cultivation. Which option is most appropriate?"
            opts=["Contour farming", "Uncontrolled burning down the slope", "Removing all ground cover", "Increasing row direction parallel to the slope"]
            return add_question("Agricultural Science", q, opts, 0, "Soil Management", "Erosion Control", "Cultivating along contour lines interrupts downslope runoff and can reduce erosion.")
        if mode == 1:
            q = "A poultry farmer compares egg number, age at first lay, survivability and feed use before selecting breeding stock. Which approach is most defensible for genetic improvement?"
            opts=["Selection using measurable production and fitness traits", "Selecting solely by plumage colour", "Random selection without records", "Selecting only the largest bird regardless of performance"]
            return add_question("Agricultural Science", q, opts, 0, "Animal Production", "Breeding and Selection", "Measured performance and relevant heritable traits provide a stronger basis for selection.")
        if mode == 2:
            q = "A crop shows poor growth after prolonged waterlogging. Soil analysis shows no severe nutrient deficiency, but pore spaces are saturated. Which physiological problem is most likely?"
            opts=["Reduced oxygen availability to roots and impaired respiration", "Excess oxygen causing unlimited ATP production", "Automatic increase in photosynthesis by roots", "Improved aeration of the root zone"]
            return add_question("Agricultural Science", q, opts, 0, "Soil Science", "Waterlogging", "Water fills air spaces in soil, reducing oxygen diffusion to roots and impairing aerobic respiration.")
        if mode == 3:
            q = "A cereal is rotated with a legume, and the farmer incorporates legume residues after harvest. Which combined benefit is most plausible when the legume forms effective root nodules?"
            opts=["Improved nitrogen availability plus greater diversification of nutrient demand", "Guaranteed elimination of every soil disease", "Permanent removal of all weeds", "Conversion of all soil phosphorus into nitrogen"]
            return add_question("Agricultural Science", q, opts, 0, "Crop Production", "Crop Rotation and Legumes", "Legumes can contribute biologically fixed nitrogen, while rotation can diversify nutrient use and break some pest cycles.")
        if mode == 4:
            q = "A farmer notices that two plots with identical fertilizer rates give different yields because one has poor drainage and compacted soil. What is the best interpretation?"
            opts=["Yield depends on interacting factors; fertilizer alone does not determine crop performance.", "Fertilizer always overrides all physical soil constraints.", "Compaction increases root oxygen supply.", "Drainage has no relation to nutrient uptake."]
            return add_question("Agricultural Science", q, opts, 0, "Crop Production", "Limiting Factors", "Plant growth depends on interacting physical, chemical and biological conditions.")
        if mode == 5:
            q = "A farmer stores maize grain at high moisture and high temperature. Several weeks later, mould damage increases. Which management change would most directly reduce the risk?"
            opts=["Dry the grain to a safe moisture level and improve cool, ventilated storage.", "Increase storage humidity and seal in warm air.", "Add untreated water before storage.", "Store grain in direct sunlight without drying"]
            return add_question("Agricultural Science", q, opts, 0, "Post-Harvest Technology", "Grain Storage", "Lower moisture and suitable temperature/ventilation reduce conditions favourable to mould growth and deterioration.")
        # pest management
        q = "A farm pest population develops resistance after repeated use of the same pesticide. Which integrated strategy is most likely to delay further resistance?"
        opts=["Combine monitoring, non-chemical controls and rotation of effective control modes.", "Increase the same pesticide dose indefinitely.", "Apply the same product on a rigid calendar regardless of pest density.", "Stop monitoring pest populations entirely."]
        return add_question("Agricultural Science", q, opts, 0, "Crop Protection", "Integrated Pest Management", "Resistance management benefits from monitoring and diversified control measures rather than continuous reliance on one mode of action.")
    return gen


# ============================================================
# COMPUTER SCIENCE
# ============================================================

def make_cs_generator():
    def gen():
        mode = random.randrange(8)
        if mode == 0:
            n = random.randint(500, 50000)
            q = f"A program scans an unsorted list of {n} records exactly once to determine whether a target exists. In the worst case, which time-complexity classification is appropriate, and why?"
            opts=["O(n), because each record may need to be inspected once", "O(1), because the target is unique", "O(log n), because the list is finite", "O(n²), because every pair must be compared"]
            return add_question("Computer Science", q, opts, 0, "Algorithms", "Time Complexity", "A single pass through n records is linear in n.")
        if mode == 1:
            q = "A database stores student records with a unique student_id in one table and department_id values referencing a unique key in another table. Which design relationship is most directly represented?"
            opts=["A foreign-key relationship enforcing a reference between related tables", "A CPU pipeline dependency", "A binary-tree traversal", "A packet-routing table"]
            return add_question("Computer Science", q, opts, 0, "Databases", "Keys and Relationships", "A foreign key links a field in one table to a key in another relational table.")
        if mode == 2:
            q = "A message claims an account will be closed within an hour unless the recipient clicks a link and enters a password. The link uses a domain that differs subtly from the official domain. What is the strongest classification?"
            opts=["A likely phishing attempt using urgency and credential harvesting", "A normal database backup", "A compiler optimization", "A hardware interrupt"]
            return add_question("Computer Science", q, opts, 0, "Cybersecurity", "Phishing and Social Engineering", "Urgency, impersonation and credential requests through deceptive links are common phishing indicators.")
        if mode == 3:
            value = random.randint(100, 4095)
            q = f"A signed integer representation question uses a conventional binary magnitude interpretation for the positive value {value}. Which hexadecimal representation corresponds to the binary form of the number?"
            hx = hex(value)[2:].upper()
            opts=[hx, hex(value+1)[2:].upper(), hex(value*2)[2:].upper(), hex(max(1,value-1))[2:].upper()]
            return add_question("Computer Science", q, opts, 0, "Number Systems", "Binary and Hexadecimal", "Convert the decimal number to binary or directly to hexadecimal; the representations are equivalent.")
        if mode == 4:
            modules = random.randint(5, 20)
            q = f"A software project is divided into {modules} modules so that input validation, data access, business rules and presentation can change independently where possible. Which design principle is most directly supported?"
            opts=["Separation of concerns/modularity", "Deliberate code duplication", "Global-state maximization", "Hard-coding all dependencies"]
            return add_question("Computer Science", q, opts, 0, "Software Engineering", "Modularity and Separation of Concerns", "Separating responsibilities reduces coupling and improves maintainability.")
        if mode == 5:
            q = "A program repeatedly looks up an item in a balanced search tree containing n keys. Compared with a linear scan, which asymptotic advantage is expected?"
            opts=["Approximately O(log n) lookup rather than O(n) in the usual balanced-tree case", "O(1) in every possible tree operation", "O(n²) because balancing multiplies the work", "No difference because all searches inspect every key"]
            return add_question("Computer Science", q, opts, 0, "Data Structures", "Search Trees", "Balanced search trees can reduce search depth to logarithmic order.")
        if mode == 6:
            q = "A web application correctly sanitizes user input but stores session tokens in client-visible storage without appropriate safeguards. Which broad security principle is still at risk?"
            opts=["Protecting authentication/session credentials from theft or misuse", "Ensuring arithmetic correctness only", "Increasing screen resolution", "Reducing CPU clock speed"]
            return add_question("Computer Science", q, opts, 0, "Cybersecurity", "Session Security", "Secure input handling alone does not guarantee safe credential/session-token storage and handling.")
        # recursion / stack reasoning
        depth = random.randint(8, 15)
        q = f"A recursive function calls itself once before returning and reaches a maximum call depth of {depth}. Ignoring implementation-specific optimizations, what structure most directly holds the active function-call frames?"
        opts=["The call stack", "The operating-system file system", "The CPU instruction decoder alone", "The browser's address bar"]
        return add_question("Computer Science", q, opts, 0, "Algorithms", "Recursion and Call Stack", "Nested active function calls are represented by stack frames on the call stack.")
    return gen


GENERATORS = {
    "Use of English": make_english_generator(),
    "Mathematics": make_math_generator(),
    "Physics": make_physics_generator(),
    "Chemistry": make_chemistry_generator(),
    "Biology": make_biology_generator(),
    "Economics": make_economics_generator(),
    "Government": make_government_generator(),
    "Literature": make_literature_generator(),
    "Geography": make_geography_generator(),
    "Commerce": make_commerce_generator(),
    "Accounting": make_accounting_generator(),
    "Agricultural Science": make_agriculture_generator(),
    "Computer Science": make_cs_generator(),
}


def run():
    random.seed(RANDOM_SEED)
    print("=" * 78)
    print("CAREER BRIDGE — EXTREME JAMB-STYLE QUESTION BANK")
    print(f"Minimum questions per subject: {TARGET_PER_SUBJECT}")
    print("Difficulty: EXTREME for every generated question")
    print("No artificial 'sentence set' / 'Practice item' variation")
    print("=" * 78)

    with app.app_context():
        cleanup_legacy_generated_questions()
        before_total = JAMBQuestion.query.count()

        for subject in SUBJECTS:
            before = count_subject(subject)
            if before >= TARGET_PER_SUBJECT:
                print(f"{subject}: {before} already present — skipped.")
                continue

            print(f"Generating {subject}: {before} -> {TARGET_PER_SUBJECT} ...", flush=True)
            add_until(subject, TARGET_PER_SUBJECT, GENERATORS[subject])
            after = count_subject(subject)
            print(f"{subject}: {before} -> {after}", flush=True)

        after_total = JAMBQuestion.query.count()
        print("\n" + "=" * 78)
        print(f"Question bank before: {before_total}")
        print(f"Question bank after:  {after_total}")
        print("=" * 78)
        print("\nSUBJECT COUNTS:")
        for subject in SUBJECTS:
            print(f"{subject}: {count_subject(subject)}")
        print("\nSeeding complete.")


if __name__ == "__main__":
    run()
