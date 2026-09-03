from datetime import datetime

from app import app, db, JAMBQuestion

# =========================================================
# CAREER BRIDGE JAMB QUESTION BANK
# =========================================================
#
# SUBJECT:
# Use of English
#
# BATCH:
# 001
#
# TOTAL QUESTIONS:
# 100
#
# SOURCE:
# Career Bridge Original
#
# IMPORTANT:
# These are original JAMB-style practice questions.
# They are NOT copied JAMB past questions.
#
# =========================================================


questions = [

    # =====================================================
    # LEXIS AND STRUCTURE
    # SYNONYMS
    # QUESTIONS 1 - 15
    # =====================================================

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Easy",
        "question": "The chairman gave a candid response to the question. What does 'candid' mean?",
        "option_a": "Angry",
        "option_b": "Frank",
        "option_c": "Uncertain",
        "option_d": "Secretive",
        "correct_answer": "B",
        "explanation": "Candid means honest, frank, or straightforward.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Easy",
        "question": "The student was reluctant to participate in the debate. What does 'reluctant' mean?",
        "option_a": "Unwilling",
        "option_b": "Excited",
        "option_c": "Prepared",
        "option_d": "Determined",
        "correct_answer": "A",
        "explanation": "Reluctant means unwilling or hesitant to do something.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Easy",
        "question": "The manager praised the diligent employee. What does 'diligent' mean?",
        "option_a": "Lazy",
        "option_b": "Careless",
        "option_c": "Hardworking",
        "option_d": "Talkative",
        "correct_answer": "C",
        "explanation": "A diligent person is hardworking and careful in carrying out tasks.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Easy",
        "question": "The villagers were delighted by the announcement. What does 'delighted' mean?",
        "option_a": "Very pleased",
        "option_b": "Very worried",
        "option_c": "Very angry",
        "option_d": "Very confused",
        "correct_answer": "A",
        "explanation": "Delighted means extremely pleased or happy.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "The witness provided an accurate account of the incident. What does 'accurate' mean?",
        "option_a": "Brief",
        "option_b": "Correct",
        "option_c": "Doubtful",
        "option_d": "Unnecessary",
        "correct_answer": "B",
        "explanation": "Accurate means correct, exact, or free from error.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "The politician's speech was vague. What does 'vague' mean?",
        "option_a": "Clear",
        "option_b": "Detailed",
        "option_c": "Unclear",
        "option_d": "Interesting",
        "correct_answer": "C",
        "explanation": "Vague means unclear, uncertain, or lacking precise detail.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "The committee decided to postpone the meeting. What does 'postpone' mean?",
        "option_a": "Cancel permanently",
        "option_b": "Bring forward",
        "option_c": "Delay",
        "option_d": "Attend",
        "correct_answer": "C",
        "explanation": "To postpone something means to delay it until a later time.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "The teacher commended the student for her excellent performance. What does 'commended' mean?",
        "option_a": "Punished",
        "option_b": "Praised",
        "option_c": "Ignored",
        "option_d": "Questioned",
        "correct_answer": "B",
        "explanation": "To commend someone means to praise them for something they have done well.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "The old building was eventually demolished. What does 'demolished' mean?",
        "option_a": "Decorated",
        "option_b": "Repaired",
        "option_c": "Pulled down",
        "option_d": "Painted",
        "correct_answer": "C",
        "explanation": "Demolished means destroyed or pulled down, especially in reference to a building.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "The company intends to acquire new equipment. What does 'acquire' mean?",
        "option_a": "Obtain",
        "option_b": "Destroy",
        "option_c": "Sell",
        "option_d": "Repair",
        "correct_answer": "A",
        "explanation": "Acquire means to obtain or gain possession of something.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "The doctor advised the patient to abstain from sugary drinks. What does 'abstain' mean?",
        "option_a": "Consume regularly",
        "option_b": "Avoid",
        "option_c": "Prepare",
        "option_d": "Purchase",
        "correct_answer": "B",
        "explanation": "Abstain means to deliberately avoid or refrain from something.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "The evidence was sufficient to support the claim. What does 'sufficient' mean?",
        "option_a": "Insufficient",
        "option_b": "Adequate",
        "option_c": "Unrelated",
        "option_d": "False",
        "correct_answer": "B",
        "explanation": "Sufficient means enough or adequate for a particular purpose.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Hard",
        "question": "The principal was meticulous when checking the examination scripts. What does 'meticulous' mean?",
        "option_a": "Extremely careful",
        "option_b": "Very impatient",
        "option_c": "Highly careless",
        "option_d": "Generally confused",
        "correct_answer": "A",
        "explanation": "Meticulous means extremely careful and attentive to details.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Hard",
        "question": "The minister's statement was ambiguous. What does 'ambiguous' mean?",
        "option_a": "Obvious",
        "option_b": "Having more than one possible meaning",
        "option_c": "Completely false",
        "option_d": "Very short",
        "correct_answer": "B",
        "explanation": "Ambiguous means open to more than one interpretation or meaning.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Synonyms",
        "difficulty": "Hard",
        "question": "The scientist was skeptical about the extraordinary claim. What does 'skeptical' mean?",
        "option_a": "Certain",
        "option_b": "Doubtful",
        "option_c": "Excited",
        "option_d": "Supportive",
        "correct_answer": "B",
        "explanation": "Skeptical means doubtful or unwilling to accept something without sufficient evidence.",
        "source": "Career Bridge Original"
    },


    # =====================================================
    # ANTONYMS
    # QUESTIONS 16 - 30
    # =====================================================

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the word opposite in meaning to 'scarce'.",
        "option_a": "Rare",
        "option_b": "Limited",
        "option_c": "Abundant",
        "option_d": "Insufficient",
        "correct_answer": "C",
        "explanation": "Scarce means available in small quantities, while abundant means plentiful.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the word opposite in meaning to 'ancient'.",
        "option_a": "Old",
        "option_b": "Modern",
        "option_c": "Historic",
        "option_d": "Traditional",
        "correct_answer": "B",
        "explanation": "Ancient refers to something very old, while modern refers to something of the present time.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the word opposite in meaning to 'expand'.",
        "option_a": "Increase",
        "option_b": "Stretch",
        "option_c": "Contract",
        "option_d": "Develop",
        "correct_answer": "C",
        "explanation": "Expand means to become larger, while contract means to become smaller.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the word opposite in meaning to 'victory'.",
        "option_a": "Success",
        "option_b": "Triumph",
        "option_c": "Defeat",
        "option_d": "Achievement",
        "correct_answer": "C",
        "explanation": "Victory means success in a contest, while defeat means losing the contest.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the word opposite in meaning to 'generous'.",
        "option_a": "Kind",
        "option_b": "Selfish",
        "option_c": "Helpful",
        "option_d": "Charitable",
        "correct_answer": "B",
        "explanation": "A generous person gives freely, while a selfish person is mainly concerned with personal interests.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the word opposite in meaning to 'permanent'.",
        "option_a": "Stable",
        "option_b": "Lasting",
        "option_c": "Temporary",
        "option_d": "Continuous",
        "correct_answer": "C",
        "explanation": "Permanent means lasting indefinitely, while temporary means lasting for only a limited period.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the word opposite in meaning to 'hostile'.",
        "option_a": "Friendly",
        "option_b": "Aggressive",
        "option_c": "Unfriendly",
        "option_d": "Violent",
        "correct_answer": "A",
        "explanation": "Hostile means unfriendly or antagonistic, while friendly is its opposite.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the word opposite in meaning to 'optimistic'.",
        "option_a": "Hopeful",
        "option_b": "Positive",
        "option_c": "Pessimistic",
        "option_d": "Confident",
        "correct_answer": "C",
        "explanation": "Optimistic means hopeful about the future, while pessimistic means expecting negative outcomes.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the word opposite in meaning to 'transparent'.",
        "option_a": "Clear",
        "option_b": "Opaque",
        "option_c": "Visible",
        "option_d": "Bright",
        "correct_answer": "B",
        "explanation": "Transparent materials allow light to pass through, while opaque materials do not.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the word opposite in meaning to 'frequent'.",
        "option_a": "Regular",
        "option_b": "Occasional",
        "option_c": "Common",
        "option_d": "Repeated",
        "correct_answer": "B",
        "explanation": "Frequent means occurring often, while occasional means occurring sometimes but not regularly.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Hard",
        "question": "Choose the word opposite in meaning to 'rigid'.",
        "option_a": "Strict",
        "option_b": "Fixed",
        "option_c": "Flexible",
        "option_d": "Firm",
        "correct_answer": "C",
        "explanation": "Rigid means stiff or inflexible, while flexible means capable of changing or bending.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Hard",
        "question": "Choose the word opposite in meaning to 'conceal'.",
        "option_a": "Hide",
        "option_b": "Reveal",
        "option_c": "Cover",
        "option_d": "Protect",
        "correct_answer": "B",
        "explanation": "Conceal means to hide something, while reveal means to make it known or visible.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Hard",
        "question": "Choose the word opposite in meaning to 'deteriorate'.",
        "option_a": "Worsen",
        "option_b": "Decline",
        "option_c": "Improve",
        "option_d": "Collapse",
        "correct_answer": "C",
        "explanation": "Deteriorate means to become worse, while improve means to become better.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Hard",
        "question": "Choose the word opposite in meaning to 'mandatory'.",
        "option_a": "Compulsory",
        "option_b": "Required",
        "option_c": "Optional",
        "option_d": "Necessary",
        "correct_answer": "C",
        "explanation": "Mandatory means required by rule or law, while optional means not compulsory.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Antonyms",
        "difficulty": "Hard",
        "question": "Choose the word opposite in meaning to 'inferior'.",
        "option_a": "Lower",
        "option_b": "Superior",
        "option_c": "Poor",
        "option_d": "Weak",
        "correct_answer": "B",
        "explanation": "Inferior means lower in quality or status, while superior means higher in quality or status.",
        "source": "Career Bridge Original"
    },


    # =====================================================
    # SENTENCE COMPLETION
    # QUESTIONS 31 - 45
    # =====================================================

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Easy",
        "question": "If Musa ______ harder, he would have passed the examination.",
        "option_a": "studies",
        "option_b": "studied",
        "option_c": "had studied",
        "option_d": "has studied",
        "correct_answer": "C",
        "explanation": "The sentence describes an unreal situation in the past, so the third conditional form 'had studied' is required.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Easy",
        "question": "Neither the teacher nor the students ______ aware of the change.",
        "option_a": "was",
        "option_b": "were",
        "option_c": "is",
        "option_d": "has",
        "correct_answer": "B",
        "explanation": "With 'neither...nor', the verb agrees with the nearer subject. 'Students' is plural, so 'were' is correct.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Easy",
        "question": "The children were punished because they ______ the classroom window.",
        "option_a": "break",
        "option_b": "have broken",
        "option_c": "had broken",
        "option_d": "will break",
        "correct_answer": "C",
        "explanation": "The breaking happened before the punishment, so the past perfect 'had broken' is appropriate.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Easy",
        "question": "She has lived in Abuja ______ 2022.",
        "option_a": "for",
        "option_b": "since",
        "option_c": "during",
        "option_d": "by",
        "correct_answer": "B",
        "explanation": "'Since' is used with a specific point in time, such as 2022.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Easy",
        "question": "The boys were tired because they ______ football for three hours.",
        "option_a": "have played",
        "option_b": "had been playing",
        "option_c": "will play",
        "option_d": "play",
        "correct_answer": "B",
        "explanation": "The past perfect continuous describes an activity that continued for a period before another past event.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Medium",
        "question": "By this time next year, I ______ my university programme.",
        "option_a": "complete",
        "option_b": "completed",
        "option_c": "will have completed",
        "option_d": "have completed",
        "correct_answer": "C",
        "explanation": "The future perfect tense is used for an action that will have been completed before a specified future time.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Medium",
        "question": "The principal, together with the teachers, ______ attending the meeting.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "The main subject is 'principal'. The phrase 'together with the teachers' does not change the singular subject.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Medium",
        "question": "I would rather you ______ the truth.",
        "option_a": "tell",
        "option_b": "told",
        "option_c": "telling",
        "option_d": "will tell",
        "correct_answer": "B",
        "explanation": "After 'would rather' when referring to another person's action, the simple past is commonly used.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Medium",
        "question": "The man was accused ______ stealing the money.",
        "option_a": "for",
        "option_b": "with",
        "option_c": "of",
        "option_d": "on",
        "correct_answer": "C",
        "explanation": "The correct expression is 'accused of' something.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Medium",
        "question": "The students congratulated their colleague ______ winning the competition.",
        "option_a": "for",
        "option_b": "on",
        "option_c": "at",
        "option_d": "with",
        "correct_answer": "B",
        "explanation": "The correct collocation is 'congratulate someone on something'.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Medium",
        "question": "Hardly had the examination started ______ the electricity went off.",
        "option_a": "than",
        "option_b": "when",
        "option_c": "then",
        "option_d": "and",
        "correct_answer": "B",
        "explanation": "The standard construction is 'hardly...when'.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Hard",
        "question": "No sooner had the guests arrived ______ the rain began.",
        "option_a": "when",
        "option_b": "than",
        "option_c": "then",
        "option_d": "and",
        "correct_answer": "B",
        "explanation": "The standard construction is 'no sooner...than'.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Hard",
        "question": "If I ______ you, I would accept the offer.",
        "option_a": "am",
        "option_b": "was",
        "option_c": "were",
        "option_d": "have been",
        "correct_answer": "C",
        "explanation": "In hypothetical statements using 'if I', the subjunctive form 'were' is traditionally used.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Hard",
        "question": "The woman insisted ______ seeing the manager.",
        "option_a": "on",
        "option_b": "at",
        "option_c": "for",
        "option_d": "with",
        "correct_answer": "A",
        "explanation": "The correct expression is 'insist on' followed by a noun or gerund.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Sentence Completion",
        "difficulty": "Hard",
        "question": "Scarcely had the teacher entered the room ______ the students became silent.",
        "option_a": "than",
        "option_b": "when",
        "option_c": "and",
        "option_d": "because",
        "correct_answer": "B",
        "explanation": "The standard construction is 'scarcely...when'.",
        "source": "Career Bridge Original"
    },


    # =====================================================
    # WORD CLASSES
    # QUESTIONS 46 - 60
    # =====================================================

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Easy",
        "question": "Identify the word class of 'quickly' in the sentence: The boy ran quickly.",
        "option_a": "Noun",
        "option_b": "Adjective",
        "option_c": "Adverb",
        "option_d": "Preposition",
        "correct_answer": "C",
        "explanation": "'Quickly' modifies the verb 'ran', so it functions as an adverb.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Easy",
        "question": "Identify the word class of 'beautiful' in the sentence: She wore a beautiful dress.",
        "option_a": "Noun",
        "option_b": "Adjective",
        "option_c": "Adverb",
        "option_d": "Verb",
        "correct_answer": "B",
        "explanation": "'Beautiful' describes the noun 'dress', so it is an adjective.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Easy",
        "question": "Identify the word class of 'honesty' in the sentence: Honesty is important.",
        "option_a": "Noun",
        "option_b": "Verb",
        "option_c": "Adjective",
        "option_d": "Adverb",
        "correct_answer": "A",
        "explanation": "'Honesty' is the name of a quality and functions as a noun.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Easy",
        "question": "Identify the word class of 'under' in the sentence: The bag is under the table.",
        "option_a": "Conjunction",
        "option_b": "Preposition",
        "option_c": "Adverb",
        "option_d": "Pronoun",
        "correct_answer": "B",
        "explanation": "'Under' shows the relationship between the bag and the table, so it is a preposition.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Easy",
        "question": "Identify the word class of 'and' in the sentence: John and Peter arrived early.",
        "option_a": "Preposition",
        "option_b": "Adverb",
        "option_c": "Conjunction",
        "option_d": "Adjective",
        "correct_answer": "C",
        "explanation": "'And' joins the words 'John' and 'Peter', so it is a conjunction.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Medium",
        "question": "Identify the word class of 'although' in the sentence: Although it rained, we continued the journey.",
        "option_a": "Conjunction",
        "option_b": "Noun",
        "option_c": "Adjective",
        "option_d": "Pronoun",
        "correct_answer": "A",
        "explanation": "'Although' introduces a subordinate clause and functions as a conjunction.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Medium",
        "question": "Identify the word class of 'carefully' in the sentence: She carefully packed the equipment.",
        "option_a": "Adjective",
        "option_b": "Adverb",
        "option_c": "Noun",
        "option_d": "Pronoun",
        "correct_answer": "B",
        "explanation": "'Carefully' describes how she packed the equipment, so it is an adverb.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Medium",
        "question": "Identify the word class of 'they' in the sentence: They arrived before noon.",
        "option_a": "Pronoun",
        "option_b": "Adjective",
        "option_c": "Conjunction",
        "option_d": "Preposition",
        "correct_answer": "A",
        "explanation": "'They' is a personal pronoun used in place of the names of people.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Medium",
        "question": "Identify the word class of 'wisdom' in the sentence: His wisdom impressed everyone.",
        "option_a": "Verb",
        "option_b": "Adverb",
        "option_c": "Noun",
        "option_d": "Adjective",
        "correct_answer": "C",
        "explanation": "'Wisdom' names a quality and therefore functions as a noun.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Medium",
        "question": "Identify the word class of 'strong' in the sentence: The athlete is strong.",
        "option_a": "Adjective",
        "option_b": "Noun",
        "option_c": "Verb",
        "option_d": "Adverb",
        "correct_answer": "A",
        "explanation": "'Strong' describes the athlete and therefore functions as an adjective.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Hard",
        "question": "Identify the word class of 'what' in the sentence: I know what you mean.",
        "option_a": "Relative pronoun",
        "option_b": "Preposition",
        "option_c": "Adverb",
        "option_d": "Adjective",
        "correct_answer": "A",
        "explanation": "'What' introduces the clause 'what you mean' and functions as a pronoun referring to the thing meant.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Hard",
        "question": "Identify the word class of 'despite' in the sentence: Despite the rain, the match continued.",
        "option_a": "Conjunction",
        "option_b": "Preposition",
        "option_c": "Adverb",
        "option_d": "Verb",
        "correct_answer": "B",
        "explanation": "'Despite' is a preposition followed by the noun phrase 'the rain'.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Hard",
        "question": "Identify the word class of 'very' in the sentence: The examination was very difficult.",
        "option_a": "Adverb",
        "option_b": "Adjective",
        "option_c": "Noun",
        "option_d": "Preposition",
        "correct_answer": "A",
        "explanation": "'Very' modifies the adjective 'difficult', so it functions as an adverb.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Hard",
        "question": "Identify the word class of 'because' in the sentence: We stayed indoors because it was raining.",
        "option_a": "Pronoun",
        "option_b": "Conjunction",
        "option_c": "Adjective",
        "option_d": "Noun",
        "correct_answer": "B",
        "explanation": "'Because' connects the main clause to a subordinate clause giving the reason.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Word Classes",
        "difficulty": "Hard",
        "question": "Identify the word class of 'running' in the sentence: Running every morning improves his fitness.",
        "option_a": "Gerund",
        "option_b": "Adjective",
        "option_c": "Preposition",
        "option_d": "Conjunction",
        "correct_answer": "A",
        "explanation": "'Running' functions as the subject of the sentence, so it is a gerund.",
        "source": "Career Bridge Original"
    },


    # =====================================================
    # CONCORD
    # QUESTIONS 61 - 75
    # =====================================================

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Easy",
        "question": "The boy ______ to school every morning.",
        "option_a": "go",
        "option_b": "goes",
        "option_c": "going",
        "option_d": "gone",
        "correct_answer": "B",
        "explanation": "The singular subject 'boy' requires the singular present-tense verb 'goes'.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Easy",
        "question": "The girls ______ preparing for the examination.",
        "option_a": "is",
        "option_b": "was",
        "option_c": "are",
        "option_d": "has",
        "correct_answer": "C",
        "explanation": "The plural subject 'girls' requires the plural verb 'are'.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Easy",
        "question": "My brother and sister ______ at home.",
        "option_a": "is",
        "option_b": "are",
        "option_c": "was",
        "option_d": "has",
        "correct_answer": "B",
        "explanation": "Two subjects joined by 'and' normally take a plural verb.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "Each of the students ______ a textbook.",
        "option_a": "have",
        "option_b": "has",
        "option_c": "having",
        "option_d": "were",
        "correct_answer": "B",
        "explanation": "'Each' is singular and therefore takes the singular verb 'has'.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "Neither of the answers ______ correct.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "'Neither' is treated as singular in formal standard English, so 'is' is appropriate.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "The news ______ encouraging.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "'News' is an uncountable singular noun and takes 'is'.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "Mathematics ______ my favourite subject.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "The name of the academic subject 'Mathematics' is treated as singular here.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "A number of students ______ absent today.",
        "option_a": "is",
        "option_b": "was",
        "option_c": "are",
        "option_d": "has",
        "correct_answer": "C",
        "explanation": "'A number of' means several and takes a plural verb.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "The number of applicants ______ increasing every year.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "'The number of' refers to one number and takes a singular verb.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Hard",
        "question": "Ten kilometres ______ a long distance to walk.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "A measurement considered as one unit takes a singular verb.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Hard",
        "question": "The committee ______ divided in its opinion.",
        "option_a": "is",
        "option_b": "are",
        "option_c": "has",
        "option_d": "was",
        "correct_answer": "B",
        "explanation": "When a collective noun refers to members acting individually, a plural verb can be used.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Hard",
        "question": "Either the teachers or the principal ______ responsible for the decision.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "With 'either...or', the verb agrees with the nearer subject. 'Principal' is singular.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Hard",
        "question": "Either the principal or the teachers ______ responsible for the decision.",
        "option_a": "is",
        "option_b": "was",
        "option_c": "are",
        "option_d": "has",
        "correct_answer": "C",
        "explanation": "The verb agrees with the nearer subject, 'teachers', which is plural.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Hard",
        "question": "The furniture in the new office ______ expensive.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "'Furniture' is an uncountable noun and takes a singular verb.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Concord",
        "difficulty": "Hard",
        "question": "Neither the students nor the teacher ______ prepared for the announcement.",
        "option_a": "were",
        "option_b": "are",
        "option_c": "was",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "The nearer subject is 'teacher', which is singular, so 'was' is required.",
        "source": "Career Bridge Original"
    },


    # =====================================================
    # IDIOMS
    # QUESTIONS 76 - 85
    # =====================================================

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Easy",
        "question": "If someone is described as 'under the weather', what does it mean?",
        "option_a": "Standing in the rain",
        "option_b": "Feeling unwell",
        "option_c": "Working outdoors",
        "option_d": "Feeling excited",
        "correct_answer": "B",
        "explanation": "The idiom 'under the weather' means feeling ill or unwell.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Easy",
        "question": "What does the expression 'break the ice' mean?",
        "option_a": "Destroy something frozen",
        "option_b": "Start a friendly conversation",
        "option_c": "End a friendship",
        "option_d": "Avoid a discussion",
        "correct_answer": "B",
        "explanation": "To break the ice means to make people feel more comfortable and begin social interaction.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Easy",
        "question": "What does 'once in a blue moon' mean?",
        "option_a": "Very frequently",
        "option_b": "Very rarely",
        "option_c": "Every evening",
        "option_d": "At midnight",
        "correct_answer": "B",
        "explanation": "The expression means something happens very rarely.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Medium",
        "question": "If a student 'hits the nail on the head', what has the student done?",
        "option_a": "Made an exact or correct statement",
        "option_b": "Made a serious mistake",
        "option_c": "Avoided the issue",
        "option_d": "Changed the subject",
        "correct_answer": "A",
        "explanation": "To hit the nail on the head means to describe or identify something exactly.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Medium",
        "question": "What does it mean to 'keep an eye on' something?",
        "option_a": "Destroy it",
        "option_b": "Watch or monitor it",
        "option_c": "Ignore it",
        "option_d": "Hide it",
        "correct_answer": "B",
        "explanation": "To keep an eye on something means to watch or monitor it carefully.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Medium",
        "question": "What does the expression 'in hot water' mean?",
        "option_a": "Swimming",
        "option_b": "In trouble",
        "option_c": "Feeling relaxed",
        "option_d": "Feeling thirsty",
        "correct_answer": "B",
        "explanation": "To be in hot water means to be in trouble or difficulty.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Medium",
        "question": "What does 'a blessing in disguise' mean?",
        "option_a": "Something that appears bad but turns out beneficial",
        "option_b": "A religious ceremony",
        "option_c": "A hidden person",
        "option_d": "A serious punishment",
        "correct_answer": "A",
        "explanation": "A blessing in disguise is something that initially seems unfortunate but eventually produces a good result.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Hard",
        "question": "If a person 'beats around the bush', what is the person doing?",
        "option_a": "Speaking directly",
        "option_b": "Avoiding the main point",
        "option_c": "Working very hard",
        "option_d": "Making a decision",
        "correct_answer": "B",
        "explanation": "To beat around the bush means to avoid addressing the main point directly.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Hard",
        "question": "What does the expression 'spill the beans' mean?",
        "option_a": "Waste food",
        "option_b": "Reveal a secret",
        "option_c": "Make a promise",
        "option_d": "Avoid responsibility",
        "correct_answer": "B",
        "explanation": "To spill the beans means to reveal secret or confidential information.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Idioms",
        "difficulty": "Hard",
        "question": "If two people 'see eye to eye', what does this mean?",
        "option_a": "They look alike",
        "option_b": "They agree with each other",
        "option_c": "They avoid each other",
        "option_d": "They compete against each other",
        "correct_answer": "B",
        "explanation": "To see eye to eye means to agree or share the same opinion.",
        "source": "Career Bridge Original"
    },


    # =====================================================
    # REGISTER
    # QUESTIONS 86 - 95
    # =====================================================

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Easy",
        "question": "Which of the following is most closely associated with the register of banking?",
        "option_a": "Deposit",
        "option_b": "Goalpost",
        "option_c": "Wicket",
        "option_d": "Surgery",
        "correct_answer": "A",
        "explanation": "'Deposit' is commonly used in banking to refer to money placed into an account.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Easy",
        "question": "Which word belongs to the register of medicine?",
        "option_a": "Invoice",
        "option_b": "Diagnosis",
        "option_c": "Goalkeeper",
        "option_d": "Mortgage",
        "correct_answer": "B",
        "explanation": "Diagnosis is a medical term referring to the identification of a disease or condition.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Easy",
        "question": "Which of the following belongs to the register of football?",
        "option_a": "Penalty",
        "option_b": "Dividend",
        "option_c": "Prescription",
        "option_d": "Affidavit",
        "correct_answer": "A",
        "explanation": "A penalty is a term commonly used in football.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Medium",
        "question": "Which of the following is associated with the register of law?",
        "option_a": "Plaintiff",
        "option_b": "Striker",
        "option_c": "Diagnosis",
        "option_d": "Dividend",
        "correct_answer": "A",
        "explanation": "A plaintiff is a person who brings a case against another person or organization in court.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Medium",
        "question": "Which of the following belongs to the register of economics?",
        "option_a": "Inflation",
        "option_b": "Syringe",
        "option_c": "Offside",
        "option_d": "Testator",
        "correct_answer": "A",
        "explanation": "Inflation is an economic term referring to a general rise in prices.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Medium",
        "question": "Which word is most closely associated with the register of aviation?",
        "option_a": "Cockpit",
        "option_b": "Mortgage",
        "option_c": "Wicket",
        "option_d": "Plaintiff",
        "correct_answer": "A",
        "explanation": "A cockpit is the area in an aircraft from which the pilot controls the aircraft.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Medium",
        "question": "Which of the following belongs to the register of accounting?",
        "option_a": "Ledger",
        "option_b": "Stethoscope",
        "option_c": "Offside",
        "option_d": "Hangar",
        "correct_answer": "A",
        "explanation": "A ledger is a book or digital record used for recording financial transactions.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Hard",
        "question": "Which of the following is associated with the register of insurance?",
        "option_a": "Premium",
        "option_b": "Dribble",
        "option_c": "Syringe",
        "option_d": "Hangar",
        "correct_answer": "A",
        "explanation": "In insurance, a premium is the amount paid for insurance coverage.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Hard",
        "question": "Which of the following belongs to the register of politics?",
        "option_a": "Electorate",
        "option_b": "Fracture",
        "option_c": "Goalpost",
        "option_d": "Ledger",
        "correct_answer": "A",
        "explanation": "The electorate refers to the people who are entitled to vote in an election.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Lexis and Structure",
        "subtopic": "Register",
        "difficulty": "Hard",
        "question": "Which of the following is associated with the register of journalism?",
        "option_a": "Headline",
        "option_b": "Ligament",
        "option_c": "Mortgage",
        "option_d": "Wicket",
        "correct_answer": "A",
        "explanation": "A headline is the title or heading of a news report and is strongly associated with journalism.",
        "source": "Career Bridge Original"
    },


    # =====================================================
    # ORAL FORMS
    # QUESTIONS 96 - 100
    # =====================================================

    {
        "subject": "Use of English",
        "topic": "Oral Forms",
        "subtopic": "Vowel Sounds",
        "difficulty": "Easy",
        "question": "Which word contains the same vowel sound as the vowel sound in 'seat'?",
        "option_a": "Sit",
        "option_b": "Set",
        "option_c": "Beat",
        "option_d": "Sat",
        "correct_answer": "C",
        "explanation": "'Seat' and 'beat' contain the long /iː/ vowel sound.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Oral Forms",
        "subtopic": "Vowel Sounds",
        "difficulty": "Easy",
        "question": "Which word contains the same vowel sound as the vowel sound in 'food'?",
        "option_a": "Good",
        "option_b": "Foot",
        "option_c": "Mood",
        "option_d": "Blood",
        "correct_answer": "C",
        "explanation": "'Food' and 'mood' contain the long /uː/ vowel sound.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Oral Forms",
        "subtopic": "Consonant Sounds",
        "difficulty": "Medium",
        "question": "Which word begins with the same consonant sound as 'chair'?",
        "option_a": "Chemist",
        "option_b": "Share",
        "option_c": "Cheap",
        "option_d": "Car",
        "correct_answer": "C",
        "explanation": "'Chair' and 'cheap' begin with the /tʃ/ sound.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Oral Forms",
        "subtopic": "Word Stress",
        "difficulty": "Medium",
        "question": "Which syllable is stressed in the noun 'PREsent' meaning a gift?",
        "option_a": "First syllable",
        "option_b": "Second syllable",
        "option_c": "Both equally",
        "option_d": "Neither syllable",
        "correct_answer": "A",
        "explanation": "As a noun meaning a gift, 'present' is normally stressed on the first syllable: PRE-sent.",
        "source": "Career Bridge Original"
    },

    {
        "subject": "Use of English",
        "topic": "Oral Forms",
        "subtopic": "Word Stress",
        "difficulty": "Hard",
        "question": "Which syllable is stressed in the verb 'reCORD'?",
        "option_a": "First syllable",
        "option_b": "Second syllable",
        "option_c": "Both equally",
        "option_d": "Neither syllable",
        "correct_answer": "B",
        "explanation": "As a verb, 'record' is stressed on the second syllable: re-CORD.",
        "source": "Career Bridge Original"
    }

]


# =========================================================
# INSERT QUESTIONS INTO DATABASE
# =========================================================

def seed_questions():

    print()
    print("=" * 60)
    print("CAREER BRIDGE JAMB QUESTION BANK")
    print("=" * 60)
    print()

    print(
        f"Questions prepared: {len(questions)}"
    )

    print()


    # -----------------------------------------------------
    # COUNT EXISTING QUESTIONS
    # -----------------------------------------------------

    existing_count = JAMBQuestion.query.count()

    print(
        f"Questions already in database: {existing_count}"
    )

    print()


    added = 0

    skipped = 0


    # -----------------------------------------------------
    # PROCESS QUESTIONS
    # -----------------------------------------------------

    for number, question_data in enumerate(
        questions,
        start=1
    ):

        question_text = question_data["question"].strip()

        subject = question_data["subject"].strip()


        # -------------------------------------------------
        # CHECK FOR DUPLICATE
        # -------------------------------------------------

        existing_question = JAMBQuestion.query.filter_by(
            question=question_text
        ).first()


        if existing_question:

            print(
                f"[SKIPPED {number:03d}] "
                f"Question already exists."
            )

            skipped += 1

            continue


        # -------------------------------------------------
        # CREATE QUESTION
        # -------------------------------------------------

        new_question = JAMBQuestion(

            subject=subject,

            topic=question_data.get(
                "topic",
                ""
            ),

            subtopic=question_data.get(
                "subtopic",
                ""
            ),

            difficulty=question_data.get(
                "difficulty",
                "Medium"
            ),

            question=question_text,

            option_a=question_data["option_a"].strip(),

            option_b=question_data["option_b"].strip(),

            option_c=question_data["option_c"].strip(),

            option_d=question_data["option_d"].strip(),

            correct_answer=question_data[
                "correct_answer"
            ].upper().strip(),

            explanation=question_data.get(
                "explanation",
                ""
            ).strip(),

            source=question_data.get(
                "source",
                "Career Bridge Original"
            ),

            year=None,

            created_at=datetime.utcnow()
            if False
            else None
        )


        # -------------------------------------------------
        # ADD TO SESSION
        # -------------------------------------------------

        db.session.add(
            new_question
        )

        added += 1


        print(
            f"[ADDED {number:03d}] "
            f"{subject} - "
            f"{question_data.get('subtopic', '')}"
        )


    # -----------------------------------------------------
    # COMMIT
    # -----------------------------------------------------

    try:

        db.session.commit()

        print()

        print(
            "=" * 60
        )

        print(
            "QUESTION BANK IMPORT COMPLETED"
        )

        print(
            "=" * 60
        )

        print(
            f"Added: {added}"
        )

        print(
            f"Skipped: {skipped}"
        )

        print(
            f"Total now in database: "
            f"{JAMBQuestion.query.count()}"
        )

        print(
            "=" * 60
        )

    except Exception as error:

        db.session.rollback()

        print()

        print(
            "ERROR WHILE SAVING QUESTIONS:"
        )

        print(
            error
        )

        raise


# =========================================================
# RUN SEEDER
# =========================================================

if __name__ == "__main__":

    with app.app_context():

        seed_questions()
