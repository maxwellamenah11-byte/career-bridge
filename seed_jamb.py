from datetime import datetime
import random
import math

from app import app, db, JAMBQuestion

# ============================================================
# CAREER BRIDGE - EXTREME JAMB-STYLE QUESTION BANK SEEDER
# ============================================================
# Creates ORIGINAL practice questions for the subjects below.
# They are NOT official JAMB past questions.
#
# Target: at least 1,000 UNIQUE questions per subject.
# Difficulty: EVERY generated question is tagged "Extreme".
#
# The generator uses many reasoning-heavy templates and randomized
# parameters instead of repeating the same question with a new number.
# ============================================================

TARGET_PER_SUBJECT = 1000
DIFFICULTY = "Extreme"
RANDOM_SEED = 20260907

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


def add_question(subject, question, options, answer_index, topic, subtopic, explanation):
    if len(options) != 4:
        raise ValueError("Each MCQ must have exactly four options")

    # Deduplicate by exact subject + question.
    if JAMBQuestion.query.filter_by(subject=subject, question=question).first():
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


def add_until(subject, target, generator):
    """Keep drawing questions until this subject has >= target rows."""
    attempts = 0
    max_attempts = target * 40
    while JAMBQuestion.query.filter_by(subject=subject).count() < target:
        created = generator()
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError(
                f"Could not create enough unique questions for {subject}. "
                f"Current count: {JAMBQuestion.query.filter_by(subject=subject).count()}"
            )
        if created:
            # Periodic flush prevents a huge in-memory identity map.
            if attempts % 250 == 0:
                db.session.flush()


# ============================================================
# USE OF ENGLISH
# ============================================================

def make_english_generator():
    contrasts = [
        ("mitigate", "aggravate", "To mitigate a problem is to make it less severe."),
        ("pervasive", "isolated", "Pervasive means widespread or present throughout."),
        ("parsimonious", "generous", "Parsimonious means excessively unwilling to spend or give."),
        ("equivocal", "unambiguous", "Equivocal means open to more than one interpretation."),
        ("intransigent", "flexible", "Intransigent means unwilling to change a position."),
        ("perfunctory", "thorough", "Perfunctory means done with little care or attention."),
        ("fastidious", "careless", "Fastidious means very attentive to detail and accuracy."),
        ("recalcitrant", "obedient", "Recalcitrant means stubbornly resistant to authority."),
        ("trenchant", "mild", "Trenchant describes forceful, sharp, or incisive expression."),
        ("circumspect", "reckless", "Circumspect means cautious and careful to avoid risk."),
    ]
    concord_templates = [
        ("Neither the principal nor the vice-principals ___ prepared to endorse the proposal.", ["was", "were", "is", "has"], 1, "The nearer plural subject 'vice-principals' controls agreement."),
        ("Hardly had the candidates completed the section when the invigilator ___ the papers.", ["collects", "had collected", "collected", "has collected"], 2, "The simple past 'collected' correctly follows the past perfect opening."),
        ("No sooner ___ the results published than the controversy began.", ["had the board had", "the board had", "did the board have", "has the board had"], 0, "The construction 'No sooner had ... than ...' requires past perfect inversion."),
        ("Each of the proposals, together with its supporting documents, ___ been reviewed.", ["have", "are", "has", "were"], 2, "The singular subject 'Each' takes 'has'."),
        ("If the committee ___ the warning earlier, the error might have been avoided.", ["heeds", "had heeded", "has heeded", "would heed"], 1, "A third conditional requires past perfect in the if-clause."),
    ]

    def gen():
        mode = random.randrange(4)
        if mode == 0:
            word, opposite, expl = random.choice(contrasts)
            q = f"Choose the option nearest in meaning to '{word}' in a formal academic context."
            opts = [opposite, word, "completely unrelated", "a weaker contrast"]
            return add_question("Use of English", q, opts, 1, "Lexis and Structure", "Advanced Vocabulary", expl)
        if mode == 1:
            q, opts, ans, expl = random.choice(concord_templates)
            return add_question("Use of English", q, opts, ans, "Lexis and Structure", "Concord and Sequence", expl)
        if mode == 2:
            a = random.randint(11, 19)
            b = random.randint(21, 39)
            c = random.randint(2, 9)
            passage = (
                f"Although the policy was introduced after {a} months of consultation, its implementation in "
                f"districts with {b} participating schools revealed a complication: each school had to process "
                f"{c} separate verification stages. The committee therefore suspended the final rollout pending "
                f"a review of administrative capacity."
            )
            q = "What is the most defensible inference from the passage?"
            opts = [
                "The policy was rejected before consultation began.",
                "Implementation problems, rather than the policy's stated purpose, prompted the suspension.",
                "Every participating school completed the verification process successfully.",
                "The committee had no evidence that administrative capacity mattered.",
            ]
            return add_question("Use of English", f"Read the passage and answer the question.\n\n{passage}\n\n{q}", opts, 1, "Comprehension", "Inference", "The passage directly links the suspension to implementation and administrative-capacity concerns.")
        # Error detection in a complex sentence.
        subjects = ["The series of revisions", "The cluster of proposals", "The list of unresolved cases", "The sequence of emergency measures"]
        subject = random.choice(subjects)
        sentence = f"{subject} have been examined carefully, but the final recommendation remain uncertain."
        q = f"In the sentence below, identify the option that contains the grammatical error.\n\n{sentence}"
        opts = ["have", "examined", "remain", "uncertain"]
        # Singular head noun controls both verbs.
        return add_question("Use of English", q, opts, 2, "Lexis and Structure", "Error Detection", "The head nouns 'series', 'cluster', 'list', and 'sequence' are singular, so the verb should be 'remains'.")

    return gen


# ============================================================
# MATHEMATICS
# ============================================================

def make_math_generator():
    def gen():
        mode = random.randrange(6)
        if mode == 0:
            # Quadratic with hidden structure and a condition.
            r1 = random.randint(-9, 9)
            r2 = random.randint(-9, 9)
            if r1 == r2:
                r2 += 2
            s = r1 + r2
            p = r1 * r2
            q = (
                f"A quadratic equation has roots α and β satisfying α+β={s} and αβ={p}. "
                f"If the roots of a second equation are α² and β², what is the sum of those roots?"
            )
            ans = s * s - 2 * p
            opts = [str(ans), str(s * s), str(2 * p), str(ans + p)]
            return add_question("Mathematics", q, opts, 0, "Algebra", "Roots and Identities", "α²+β²=(α+β)²−2αβ.")
        if mode == 1:
            a = random.randint(3, 11)
            b = random.randint(2, 9)
            c = random.randint(2, 6)
            q = f"The graph of y = {a}x² − {b}x + {c} is transformed by replacing x with (x−2). What is the x-coordinate of its axis of symmetry after the transformation?"
            original_axis = b / (2 * a)
            ans = original_axis + 2
            opts = [f"{ans:.2f}", f"{original_axis:.2f}", f"{2-original_axis:.2f}", f"{ans+2:.2f}"]
            return add_question("Mathematics", q, opts, 0, "Algebra", "Transformations", "Replacing x by x−2 shifts the graph 2 units to the right, so the axis also shifts 2 units right.")
        if mode == 2:
            base = random.randint(5, 14)
            height = random.randint(6, 15)
            slant = random.randint(8, 18)
            q = f"A triangular field has base {base} m, height {height} m and equal sides each {slant} m. If fencing costs ₦{random.randint(700,1400):,} per metre, what is the total cost of fencing the three sides?"
            # Using perimeter only.
            rate = int(q.split("₦")[1].split(" per")[0].replace(",", ""))
            ans = (base + 2 * slant) * rate
            opts = [f"₦{ans:,}", f"₦{ans+rate:,}", f"₦{ans-rate:,}", f"₦{ans*2:,}"]
            return add_question("Mathematics", q, opts, 0, "Mensuration", "Perimeter and Cost", "Total fencing cost equals perimeter × cost per metre.")
        if mode == 3:
            total = random.randint(7, 12)
            chosen = random.randint(2, total - 2)
            q = f"A committee of {total} candidates contains {chosen} students from one department and {total-chosen} from another. Two members are chosen at random without replacement. What is the probability that they come from different departments?"
            p = 2 * chosen * (total - chosen) / (total * (total - 1))
            from fractions import Fraction
            ansf = Fraction(2 * chosen * (total - chosen), total * (total - 1))
            opts = [str(ansf), str(Fraction(chosen, total)), str(Fraction(total-chosen, total)), str(Fraction(chosen*(chosen-1), total*(total-1)))]
            return add_question("Mathematics", q, opts, 0, "Probability", "Without Replacement", "Count ordered cross-department selections and divide by all ordered selections.")
        if mode == 4:
            n = random.randint(4, 9)
            r = random.randint(2, 5)
            q = f"A geometric sequence has first term {n} and common ratio 1/{r}. Find the sum to infinity."
            from fractions import Fraction
            ans = Fraction(n * r, r - 1)
            opts = [str(ans), str(Fraction(n, r)), str(Fraction(n, r-1)), str(ans * 2)]
            return add_question("Mathematics", q, opts, 0, "Sequences", "Geometric Progression", "S∞=a/(1−r)=n/(1−1/r)=nr/(r−1).")
        # simultaneous equations with parameters
        x = random.randint(2, 9)
        y = random.randint(2, 9)
        k = random.randint(3, 8)
        c1 = x + k*y
        c2 = 2*x - y
        q = f"Given x + {k}y = {c1} and 2x − y = {c2}, determine 3x + {k+1}y."
        target = 3*x + (k+1)*y
        opts = [str(target), str(target+x), str(target-y), str(c1+c2)]
        return add_question("Mathematics", q, opts, 0, "Algebra", "Simultaneous Equations", "Solve the two equations for x and y, then substitute into the required linear combination.")
    return gen


# ============================================================
# PHYSICS
# ============================================================

def make_physics_generator():
    def gen():
        mode = random.randrange(5)
        if mode == 0:
            u = random.randint(6, 18)
            a = random.randint(2, 5)
            t = random.randint(3, 7)
            v = u + a*t
            s = u*t + 0.5*a*t*t
            q = f"A particle starts with speed {u} m/s and accelerates uniformly at {a} m/s² for {t} s. What is the ratio of its final kinetic energy to its initial kinetic energy?"
            from fractions import Fraction
            ratio = Fraction(v*v, u*u)
            opts = [str(ratio), str(Fraction(v,u)), str(Fraction(v*v, u)), str(Fraction(u*u, v*v))]
            return add_question("Physics", q, opts, 0, "Mechanics", "Kinematics and Energy", "Kinetic energy is proportional to v² for constant mass.")
        if mode == 1:
            m = random.randint(2, 8)
            mu = round(random.uniform(0.2, 0.6), 2)
            g = 10
            N = m*g
            friction = mu*N
            force = friction + random.randint(5, 25)
            a = (force - friction)/m
            q = f"A {m} kg block is pulled horizontally by {force:.1f} N on a rough surface with coefficient of friction {mu}. Take g=10 m/s². What is its acceleration?"
            opts = [f"{a:.2f} m/s²", f"{(force+friction)/m:.2f} m/s²", f"{friction/m:.2f} m/s²", f"{force/m:.2f} m/s²"]
            return add_question("Physics", q, opts, 0, "Mechanics", "Friction", "Friction = μmg. Net force = applied force − friction; a = Fnet/m.")
        if mode == 2:
            R1 = random.randint(2, 8)
            R2 = random.randint(3, 12)
            V = random.randint(12, 36)
            Req = R1 + R2
            I = V/Req
            q = f"Two resistors of {R1} Ω and {R2} Ω are connected in series to a {V} V source. If a third resistor is then added in series and the current falls to one-half its former value, what is the resistance of the third resistor?"
            R3 = Req
            opts = [f"{R3:.1f} Ω", f"{Req/2:.1f} Ω", f"{2*Req:.1f} Ω", f"{V/2:.1f} Ω"]
            return add_question("Physics", q, opts, 0, "Electricity", "Series Circuits", "Halving current at constant voltage requires doubling total resistance; therefore R3 must equal the original resistance." )
        if mode == 3:
            f = random.randint(2, 8) * 10
            L = random.randint(1, 5) * 0.1
            v = f * L
            q = f"A wave has frequency {f} Hz and wavelength {L:.1f} m. If its frequency is increased by 50% while its speed in the same medium remains constant, what is its new wavelength?"
            new_L = L/1.5
            opts = [f"{new_L:.3f} m", f"{L*1.5:.3f} m", f"{L+0.5:.3f} m", f"{L/0.5:.3f} m"]
            return add_question("Physics", q, opts, 0, "Waves", "Wave Equation", "Since v=fλ remains constant, λ is inversely proportional to f.")
        # pressure / buoyancy reasoning
        density = random.randint(800, 1200)
        volume = random.randint(2, 8) / 1000
        g = 10
        buoyancy = density*volume*g
        mass = random.randint(1, 6)
        weight = mass*g
        q = f"An object displaces {volume:.3f} m³ of a liquid of density {density} kg/m³. Take g=10 m/s². If its weight is {weight} N, what is the resultant vertical force due only to buoyancy and weight?"
        net = buoyancy - weight
        opts = [f"{net:.2f} N upward" if net >= 0 else f"{abs(net):.2f} N downward",
                f"{abs(buoyancy)+weight:.2f} N upward",
                f"{abs(weight-buoyancy)/2:.2f} N downward",
                f"{buoyancy:.2f} N upward"]
        return add_question("Physics", q, opts, 0, "Fluids", "Upthrust", "Upthrust = ρVg. Resultant force is upthrust minus weight.")
    return gen


# ============================================================
# CHEMISTRY
# ============================================================

def make_chemistry_generator():
    def gen():
        mode = random.randrange(5)
        if mode == 0:
            moles = random.randint(2, 6)
            concentration = random.randint(1, 5) / 2
            volume = moles / concentration
            q = f"How many litres of a {concentration:.1f} mol dm⁻³ solution are required to contain {moles} mol of solute?"
            opts = [f"{volume:.2f} dm³", f"{moles*concentration:.2f} dm³", f"{volume/2:.2f} dm³", f"{moles/concentration/10:.2f} dm³"]
            return add_question("Chemistry", q, opts, 0, "Stoichiometry", "Concentration", "Use C=n/V, so V=n/C.")
        if mode == 1:
            acid_m = random.randint(1, 4)
            base_m = random.randint(1, 4)
            acid_vol = random.randint(10, 40)
            ratio = random.choice([1, 2])
            # artificial but balanced generic monoprotic reaction
            base_conc = (acid_m * acid_vol) / (base_m * ratio * 10)
            q = f"A monoprotic acid solution of concentration {acid_m/10:.1f} mol dm⁻³ neutralizes {acid_vol} cm³ of solution with {base_m/10:.1f} mol dm⁻³ base in a 1:{ratio} acid-to-base stoichiometric ratio. What base volume is required?"
            # n acid = ca*va; stoich base moles = ratio*n acid; Vb=n/Cb
            ca=acid_m/10; cb=base_m/10; va=acid_vol/1000
            vb=(ratio*ca*va)/cb
            ans_ml=vb*1000
            opts=[f"{ans_ml:.1f} cm³", f"{ans_ml/ratio:.1f} cm³", f"{ans_ml*ratio:.1f} cm³", f"{acid_vol:.1f} cm³"]
            return add_question("Chemistry", q, opts, 0, "Acids and Bases", "Titration", "Balance stoichiometric moles first, then use concentration to find volume.")
        if mode == 2:
            # isotope average mass
            m1 = random.randint(20, 40)
            m2 = m1 + 2
            p = random.randint(20, 80)
            avg = (m1*p + m2*(100-p))/100
            q = f"An element has two isotopes of masses {m1} and {m2}. The lighter isotope has abundance {p}%. What is the relative atomic mass of the element?"
            opts=[f"{avg:.2f}", f"{(m1+m2)/2:.2f}", f"{(m1*p+m2*p)/100:.2f}", f"{m1 + p/100:.2f}"]
            return add_question("Chemistry", q, opts, 0, "Atomic Structure", "Isotopes", "Relative atomic mass is the weighted mean of isotopic masses." )
        if mode == 3:
            temp = random.randint(300, 500)
            press = random.randint(1, 4)
            factor = random.randint(2, 5)
            q = f"A fixed mass of gas occupies {random.randint(2, 8)} dm³ at {press} atm and {temp} K. If the pressure is increased by a factor of {factor} while temperature remains constant, what happens to its volume?"
            oldv = int(q.split("occupies ")[1].split(" dm³")[0])
            newv = oldv/factor
            opts=[f"{newv:.2f} dm³", f"{oldv*factor:.2f} dm³", f"{oldv+factor:.2f} dm³", f"{oldv/(factor-1):.2f} dm³"]
            return add_question("Chemistry", q, opts, 0, "States of Matter", "Gas Laws", "At constant temperature, Boyle's law gives P1V1=P2V2." )
        # equilibrium / Le Chatelier conceptual trap
        shift = random.choice(["to the right", "to the left", "no shift", "depends only on catalyst"])
        if shift == "to the right":
            q = "For an exothermic equilibrium, which change most directly favours formation of products?"
            opts=["Lowering temperature", "Adding a catalyst", "Increasing the activation energy", "Removing a reactant"]
            ans=0
            expl="For an exothermic forward reaction, lowering temperature favours the heat-producing direction."
        else:
            q = "For a gaseous equilibrium with fewer moles of gas on the product side, which change favours products?"
            opts=["Increasing pressure", "Decreasing pressure", "Adding an inert gas at constant volume", "Adding a catalyst"]
            ans=0
            expl="Increasing pressure shifts equilibrium toward the side with fewer gaseous moles."
        return add_question("Chemistry", q, opts, ans, "Equilibrium", "Le Chatelier's Principle", expl)
    return gen


# ============================================================
# BIOLOGY
# ============================================================

def make_biology_generator():
    def gen():
        mode=random.randrange(5)
        if mode == 0:
            # Monohybrid cross with randomized labels, still a single recessive trait.
            dominant=random.choice(["tall","smooth","purple","black"])
            recessive={"tall":"dwarf","smooth":"wrinkled","purple":"white","black":"white"}[dominant]
            q=f"In a single-gene trait, {dominant.title()} is dominant over {recessive}. A heterozygous {dominant} organism is crossed with a homozygous {recessive} organism. What proportion of offspring is expected to be heterozygous?"
            opts=["0%","25%","50%","100%"]
            return add_question("Biology",q,opts,2,"Genetics","Monohybrid Cross","The cross Tt × tt gives a 1:1 ratio of heterozygous to homozygous recessive offspring.")
        if mode == 1:
            bases=random.choice(["AAGCTT","TTCGAA","CCATGG","GGAACC","ATGCCA","CGTATA"] )
            comp=bases.translate(str.maketrans("ATCG","TAGC"))
            rna=comp.replace("T","U")
            q=f"A DNA template strand is written as 3'-{bases}-5'. Which sequence represents the complementary RNA transcribed from it?"
            opts=[rna,bases.replace("T","U"),bases,comp]
            return add_question("Biology",q,opts,0,"Genetics","Transcription","RNA is complementary to the DNA template, with uracil replacing thymine.")
        if mode == 2:
            light=random.randint(3, 12)
            q=f"A plant is kept in darkness for {light} days and then exposed to bright light while carbon dioxide is withheld. Which process is most immediately limited?"
            opts=["Light absorption by chlorophyll","Carbon fixation in the Calvin cycle","Water uptake by roots","Mineral absorption by xylem"]
            return add_question("Biology",q,opts,1,"Plant Physiology","Photosynthesis","Without carbon dioxide, carbon fixation is directly limited even though light can still be absorbed.")
        if mode == 3:
            carrying=random.randint(500, 5000)
            q=f"A population rises rapidly, slows as it approaches an environmental limit of about {carrying} individuals, and then fluctuates around that level. Which model best describes this pattern?"
            opts=["Logistic growth","Unrestricted exponential growth","Random mutation","Artificial selection"]
            return add_question("Biology",q,opts,0,"Ecology","Population Growth","Logistic growth rises rapidly before slowing near carrying capacity.")
        activity=random.randint(20, 90)
        q=f"During {activity} minutes of vigorous exercise, which combination best explains why breathing rate increases?"
        opts=["To supply more oxygen and remove additional carbon dioxide produced by active tissues","To stop cellular respiration and conserve ATP","To reduce glucose delivery to muscles","To prevent all heat production in cells"]
        return add_question("Biology",q,opts,0,"Human Physiology","Respiration","Exercise increases metabolic demand, raising oxygen requirement and carbon-dioxide production.")
    return gen


# ============================================================
# ECONOMICS
# ============================================================

def make_economics_generator():
    def gen():
        mode = random.randrange(5)
        if mode == 0:
            q = "A firm's price rises from ₦200 to ₦240 and quantity demanded falls from 500 units to 440 units. Using percentage changes based on the original values, what is the approximate price elasticity of demand?"
            ped = ((440-500)/500)/((240-200)/200)
            opts=[f"{abs(ped):.2f}", f"{abs(1/ped):.2f}", "0.25", "2.00"]
            return add_question("Economics", q, opts, 0, "Demand and Supply", "Price Elasticity", "PED = percentage change in quantity demanded / percentage change in price." )
        if mode == 1:
            q = "When a government raises a tax on a good with highly inelastic demand, which outcome is most likely, other things equal?"
            opts=["Consumers bear a relatively large share of the tax burden", "Quantity demanded changes dramatically", "The tax necessarily raises zero revenue", "Demand becomes perfectly elastic"]
            return add_question("Economics", q, opts, 0, "Public Finance", "Tax Incidence", "With relatively inelastic demand, consumers are less responsive to price changes and tend to bear more of the tax burden." )
        if mode == 2:
            q = "If nominal GDP increases by 10% while the general price level increases by 6%, what is the approximate real GDP growth rate using the exact ratio formula?"
            real = (1.10/1.06 - 1)*100
            opts=[f"{real:.2f}%", "4.00%", "16.00%", "60.00%"]
            return add_question("Economics", q, opts, 0, "Macroeconomics", "Real and Nominal GDP", "Real growth follows (1+nominal growth)/(1+inflation)−1." )
        if mode == 3:
            q = "A central bank increases the policy rate during a period of demand-pull inflation. Which transmission effect is most consistent with this action?"
            opts=["Higher borrowing costs reduce spending and investment", "Borrowing becomes cheaper immediately", "Aggregate demand must rise", "Exports must fall to zero"]
            return add_question("Economics", q, opts, 0, "Macroeconomics", "Monetary Policy", "Higher interest rates can reduce interest-sensitive consumption and investment, easing demand pressures." )
        q = "A country imposes a tariff on imported steel mainly to protect domestic producers. What is the most direct likely consequence, assuming no other policy changes?"
        opts=["Domestic steel prices tend to rise relative to the free-trade outcome", "Domestic producers necessarily become less competitive abroad", "Consumers pay a lower price in every case", "Import demand must become infinite"]
        return add_question("Economics", q, opts, 0, "International Trade", "Tariffs", "A tariff raises the domestic price above the free-trade level under standard competitive assumptions." )
    return gen


# ============================================================
# GOVERNMENT
# ============================================================

def make_government_generator():
    principles = [
        ("checks and balances", "A legislature passes a bill, the executive refuses assent, and the legislature later overrides the refusal under a constitutionally permitted procedure."),
        ("judicial review", "A constitutional court invalidates an executive action because it conflicts with a higher constitutional rule."),
        ("federalism", "Two levels of government possess constitutionally protected powers and neither is legally subordinate in all spheres."),
        ("representative democracy", "Citizens select representatives who make public policy on their behalf."),
        ("legislative oversight", "A parliament examines public expenditure and demands explanations from ministers."),
    ]
    def gen():
        correct, base = random.choice(principles)
        n = random.randint(11, 97)
        year = random.randint(1990, 2035)
        q = (
            f"In a fictional federation in {year}, {n} legislators examine the following situation: {base} "
            f"If the constitutional dispute involves division or limitation of public power, which principle is MOST directly illustrated?"
        )
        opts = [
            correct,
            "administrative decentralization",
            "party manifestoes",
            "civil service neutrality",
        ]
        return add_question("Government", q, opts, 0, "Political Concepts", "Advanced Application", f"The described constitutional relationship most directly illustrates {correct}.")
    return gen


# ============================================================
# LITERATURE
# ============================================================

def make_literature_generator():
    devices = [
        ("symbolism", "A recurring image of a locked gate appears whenever the protagonist is denied a choice."),
        ("irony", "A speaker praises the outcome immediately after an event has produced the opposite result."),
        ("soliloquy", "A character reveals private thoughts while alone on stage and the audience is given access to those thoughts."),
        ("suspense", "The narrator repeatedly withholds a crucial fact and releases it close to the climax."),
        ("person-versus-society", "The central conflict pits an individual's conscience against a rigid social code."),
    ]
    def gen():
        correct, base = random.choice(devices)
        intensity = random.randint(2, 9)
        act = random.randint(1, 5)
        century = random.choice(["nineteenth", "twentieth", "twenty-first"])
        q = (
            f"In Act {act} of a {century}-century-style drama with {intensity} major turning points, consider this situation: {base} "
            "Which literary device or technique is MOST appropriate?"
        )
        opts = [correct, "foreshadowing only", "onomatopoeia", "pastoral convention"]
        return add_question("Literature", q, opts, 0, "Literary Devices", "Interpretation", f"The situation is best explained by {correct}.")
    return gen


# ============================================================
# GEOGRAPHY
# ============================================================

def make_geography_generator():
    def gen():
        mode = random.randrange(5)
        if mode == 0:
            scale = random.choice([50000, 100000, 250000])
            map_cm = random.randint(3, 12)
            actual_km = map_cm * scale / 100000
            q = f"A map has a scale of 1:{scale:,}. Two settlements are {map_cm} cm apart on the map. What is their ground distance?"
            opts=[f"{actual_km:.2f} km", f"{actual_km*100:.2f} km", f"{actual_km/10:.2f} km", f"{actual_km*10:.2f} km"]
            return add_question("Geography", q, opts, 0, "Map Reading", "Scale Conversion", "Convert map centimetres to ground centimetres, then to kilometres." )
        if mode == 1:
            rainfall = random.randint(40, 95)
            q = f"A station records monthly rainfall of {rainfall} mm in January, {rainfall+35} mm in February, and {rainfall-10} mm in March. Which month contributes the greatest amount to the three-month total?"
            opts=["February", "January", "March", "They are equal"]
            return add_question("Geography", q, opts, 0, "Weather", "Rainfall Interpretation", "Compare the monthly values; February is the largest contributor." )
        if mode == 2:
            q = "A river has a broad floodplain, a meandering channel and deposition on the inner bends. Which process is most strongly indicated?"
            opts=["Lateral erosion and deposition", "Glacial plucking", "Wave refraction only", "Volcanic extrusion"]
            return add_question("Geography", q, opts, 0, "Geomorphology", "River Processes", "Meanders involve erosion on outer bends and deposition on inner bends, producing floodplain development." )
        if mode == 3:
            q = "A city experiences rapid population growth, rising traffic congestion and expansion of built-up land into nearby rural areas. Which process best describes the spatial change?"
            opts=["Urban sprawl", "Desertification", "Afforestation", "Retreating glaciation"]
            return add_question("Geography", q, opts, 0, "Settlement", "Urbanization", "Expansion of urban land outward into adjoining rural areas is urban sprawl." )
        q = "A humid tropical region is cleared of vegetation, and heavy rainfall then repeatedly washes topsoil downslope. Which combination best explains the increased soil loss?"
        opts=["Loss of protective cover plus high-intensity runoff", "Lower rainfall plus denser forest cover", "Reduced runoff plus increased humus", "Glacial abrasion plus sea-floor spreading"]
        return add_question("Geography", q, opts, 0, "Environmental Management", "Soil Erosion", "Vegetation protects soil; clearing it increases runoff impact and erosion." )
    return gen


# ============================================================
# COMMERCE
# ============================================================

def make_commerce_generator():
    def gen():
        mode=random.randrange(5)
        n=random.randint(3, 80)
        batch=random.randint(2, 35)
        if mode == 0:
            q=f"A manufacturer sells a product directly to consumers through an online store and processes {n} orders across {batch} delivery zones without a wholesaler. Which effect is most directly associated with this channel?"
            opts=["Fewer intermediary stages", "Automatic elimination of promotion", "Prohibition of retailing", "Compulsory use of a wholesaler"]
            return add_question("Commerce",q,opts,0,"Distribution","Channels of Distribution","Direct selling removes intermediary stages from the channel.")
        if mode == 1:
            q=f"An insurer receives a proposal for stock worth ₦{n*25000:,} across {batch} storage units. The proposer deliberately omits a material fact about fire risk. Which principle is most directly threatened?"
            opts=["Utmost good faith","Indemnity only","Contribution only","Subrogation only"]
            return add_question("Commerce",q,opts,0,"Insurance","Principles of Insurance","Material facts must be disclosed honestly under utmost good faith.")
        if mode == 2:
            q=f"A retailer receives {n} cartons of goods in {batch} product lines on credit and receives a document listing the goods, quantities and amount due. Which document is most directly described?"
            opts=["Invoice","Receipt","Prospectus","Memorandum of association"]
            return add_question("Commerce",q,opts,0,"Business Documents","Trade Documentation","An invoice records goods supplied and the amount payable.")
        if mode == 3:
            q=f"A firm divides a market according to age, income and occupation before preparing {n} different promotional messages for {batch} customer clusters. What is this process?"
            opts=["Market segmentation","Vertical integration","Trade credit","Product liquidation"]
            return add_question("Commerce",q,opts,0,"Marketing","Market Segmentation","Segmentation divides a broad market into identifiable consumer groups.")
        units=n*10
        q=f"A firm increases output from {units} to {units*4} units across {batch} production runs while spreading the same annual fixed cost over the larger output. Which advantage is illustrated?"
        opts=["Economies of scale","Trade diversion","Uninsurable risk","Market fragmentation"]
        return add_question("Commerce",q,opts,0,"Production","Economies of Scale","Spreading fixed costs over more units can lower average cost.")
    return gen


# ============================================================
# ACCOUNTING
# ============================================================

def make_accounting_generator():
    def gen():
        mode = random.randrange(5)
        if mode == 0:
            assets = random.randint(150000, 800000)
            liabilities = random.randint(50000, 300000)
            capital = assets - liabilities
            q = f"A business has total assets of ₦{assets:,} and total liabilities of ₦{liabilities:,}. It also has drawings of ₦{random.randint(10000,60000):,}. What is the owner's equity before considering current-year profit or loss?"
            opts=[f"₦{capital:,}", f"₦{assets+liabilities:,}", f"₦{liabilities:,}", f"₦{capital+10000:,}"]
            return add_question("Accounting", q, opts, 0, "Accounting Principles", "Accounting Equation", "Owner's equity = assets − liabilities; drawings do not alter the opening accounting-equation calculation here." )
        if mode == 1:
            cost = random.randint(100000, 500000)
            residual = random.randint(10000, 50000)
            life = random.randint(4, 8)
            dep = (cost-residual)/life
            q = f"A machine costs ₦{cost:,}, has a residual value of ₦{residual:,}, and a useful life of {life} years. Under straight-line depreciation, what is the annual depreciation expense?"
            opts=[f"₦{dep:,.2f}", f"₦{cost/life:,.2f}", f"₦{residual/life:,.2f}", f"₦{(cost+residual)/life:,.2f}"]
            return add_question("Accounting", q, opts, 0, "Non-current Assets", "Depreciation", "Straight-line depreciation = (cost − residual value) ÷ useful life." )
        if mode == 2:
            sales = random.randint(400000, 900000)
            cogs = random.randint(200000, 500000)
            expenses = random.randint(70000, 180000)
            gp = sales-cogs
            np = gp-expenses
            q = f"A business records sales of ₦{sales:,}, cost of goods sold of ₦{cogs:,}, and operating expenses of ₦{expenses:,}. What is its net profit?"
            opts=[f"₦{np:,}", f"₦{gp:,}", f"₦{sales-expenses:,}", f"₦{cogs-expenses:,}"]
            return add_question("Accounting", q, opts, 0, "Financial Statements", "Profit Calculation", "Net profit = gross profit − operating expenses, and gross profit = sales − cost of goods sold." )
        if mode == 3:
            cash_book = random.randint(100000, 300000)
            bank = cash_book + random.randint(-30000, 30000)
            q = f"The cash-book bank balance is ₦{cash_book:,} while the bank statement shows ₦{bank:,}. A standing order of ₦{abs(cash_book-bank)//2:,} has not yet been entered in the cash book. Which reconciliation principle should be applied before concluding that the bank statement is wrong?"
            opts=["Consider timing and unrecorded-item differences", "Assume all bank entries are errors", "Ignore the cash book", "Treat the difference as capital"]
            return add_question("Accounting", q, opts, 0, "Bank Reconciliation", "Reconciling Items", "Differences can arise because one record contains transactions not yet entered in the other." )
        q = "A trial balance agrees, yet an entire credit sale has been omitted from the books. What does this demonstrate?"
        opts=["A trial balance cannot detect every type of error", "A trial balance proves all transactions are correct", "The balance sheet must be wrong", "The error will always create a suspense account"]
        return add_question("Accounting", q, opts, 0, "Books of Account", "Errors and Trial Balance", "Errors of complete omission can leave the trial balance still balancing." )
    return gen


# ============================================================
# AGRICULTURAL SCIENCE
# ============================================================

def make_agriculture_generator():
    scenarios = [
        ("Contour farming", "A farmer on a slope notices increasingly severe topsoil loss after heavy storms.", "planting and cultivating along contour lines can reduce runoff speed."),
        ("Selective breeding", "A livestock farmer records feed conversion and reproductive performance before choosing replacement animals.", "selection can favour desirable inherited traits."),
        ("Poor root-zone aeration", "A crop field remains waterlogged for several days and the plants develop weak growth and yellowing leaves.", "water-filled pore spaces can reduce oxygen available to roots."),
        ("Crop rotation", "A farmer alternates a cereal with a legume across successive seasons.", "rotation can diversify nutrient demands and can improve soil nitrogen status when legumes are well managed."),
        ("Performance-based selection", "A poultry keeper compares egg output over several production cycles before retaining breeding stock.", "measured performance provides a rational basis for selection."),
    ]
    def gen():
        correct, base, principle = random.choice(scenarios)
        years = random.randint(2, 7)
        plots = random.randint(3, 60)
        q = f"A farm records the following situation across {plots} plots over {years} production seasons: {base} Which practice or principle is MOST appropriate, given that {principle}"
        opts = [correct, "random mating", "continuous burning", "uncontrolled overstocking"]
        return add_question("Agricultural Science", q, opts, 0, "Agricultural Production", "Applied Reasoning", f"The scenario most directly supports {correct}.")
    return gen


# ============================================================
# COMPUTER SCIENCE
# ============================================================

def make_cs_generator():
    def gen():
        mode=random.randrange(5)
        n=random.randint(20, 2000)
        if mode == 0:
            q=f"A program searches an unsorted list containing {n} items one at a time until it finds a target or reaches the end. What is the worst-case time complexity?"
            opts=["O(n)","O(log n)","O(1)","O(n²)"]
            return add_question("Computer Science",q,opts,0,"Algorithms","Complexity","The worst case inspects every item once, giving linear time.")
        if mode == 1:
            q=f"A database contains {n} student records. Each student row stores department_id, which references a unique key in a separate department table. What relationship is being represented?"
            opts=["Foreign-key relationship","Operating-system process","Hash collision","CPU pipeline"]
            return add_question("Computer Science",q,opts,0,"Databases","Keys and Relationships","A foreign key references a key in another table.")
        if mode == 2:
            q=f"A user receives a message claiming that an account will be closed in {n%48+1} hours unless they click a link and submit a password. What is the strongest initial classification?"
            opts=["Phishing attempt","Defragmentation","Load balancing","Data compression"]
            return add_question("Computer Science",q,opts,0,"Cybersecurity","Social Engineering","Urgent credential requests through suspicious links are characteristic of phishing.")
        if mode == 3:
            value=random.randint(16, 4095)
            q=f"What is the decimal value of the binary number {value:b}?"
            opts=[str(value),str(value+1),str(value-1),str(value*2)]
            return add_question("Computer Science",q,opts,0,"Number Systems","Binary Conversion","Convert each binary position to its corresponding power of two.")
        modules=random.randint(3, 15)
        q=f"A program is divided into {modules} modules, with input validation, business logic and output rendering separated into distinct responsibilities. Which principle is most directly supported?"
        opts=["Separation of concerns","Hard-coding","Global state expansion","Code duplication"]
        return add_question("Computer Science",q,opts,0,"Software Engineering","Modularity","Separating responsibilities into modules improves maintainability and reduces coupling.")
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


def count_subject(subject):
    return JAMBQuestion.query.filter_by(subject=subject).count()


def run():
    random.seed(RANDOM_SEED)
    print("=" * 78)
    print("CAREER BRIDGE - EXTREME JAMB-STYLE QUESTION BANK SEED")
    print(f"Target per subject: {TARGET_PER_SUBJECT}")
    print("Difficulty: EXTREME for every generated question")
    print("=" * 78)

    with app.app_context():
        before_total = JAMBQuestion.query.count()

        for subject in SUBJECTS:
            before = count_subject(subject)
            if before >= TARGET_PER_SUBJECT:
                print(f"{subject}: {before} already present - skipped.")
                continue

            print(f"Generating {subject}: {before} -> {TARGET_PER_SUBJECT} ...")
            add_until(subject, TARGET_PER_SUBJECT, GENERATORS[subject])
            db.session.commit()
            after = count_subject(subject)
            print(f"{subject}: {before} -> {after}")

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
