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
    """Keep generating questions until the subject reaches the target.

    Malformed generated MCQs (for example, duplicate answer options) are
    skipped and retried instead of stopping the entire seed process.
    """
    existing = count_subject(subject)
    attempts = 0
    skipped = 0
    max_attempts = max(50000, (target - existing) * 120)

    while count_subject(subject) < target:
        attempts += 1
        if attempts > max_attempts:
            raise RuntimeError(
                f"Could not reach {target} questions for {subject}. "
                f"Only {count_subject(subject)} were created after {attempts} attempts "
                f"({skipped} malformed/failed generations skipped)."
            )

        try:
            generator()
        except ValueError as exc:
            skipped += 1
            db.session.rollback()
            print(f"  Skipping malformed {subject} question: {exc}", flush=True)
            continue
        except Exception as exc:
            skipped += 1
            db.session.rollback()
            print(f"  Skipping failed {subject} question: {exc}", flush=True)
            continue

        if attempts % 100 == 0:
            db.session.flush()

        if attempts % 500 == 0:
            db.session.commit()

    db.session.commit()

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
