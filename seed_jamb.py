from app import app, db, JAMBQuestion


# =========================================================
# CAREER BRIDGE — USE OF ENGLISH QUESTION BANK
# =========================================================
#
# 100 ORIGINAL JAMB-STYLE USE OF ENGLISH QUESTIONS
#
# These are practice questions created for Career Bridge.
# They are NOT official JAMB past questions.
#
# =========================================================


ENGLISH_QUESTIONS = [

    # =====================================================
    # GRAMMAR / LEXIS
    # =====================================================

    {
        "topic": "Grammar",
        "subtopic": "Tenses",
        "difficulty": "Easy",
        "question": "By the time we arrived at the station, the train ____.",
        "option_a": "leaves",
        "option_b": "had left",
        "option_c": "has left",
        "option_d": "will leave",
        "correct_answer": "B",
        "explanation": "The past perfect 'had left' shows that the train left before another past action."
    },

    {
        "topic": "Grammar",
        "subtopic": "Tenses",
        "difficulty": "Easy",
        "question": "She ____ in Lagos since 2021.",
        "option_a": "lives",
        "option_b": "lived",
        "option_c": "has lived",
        "option_d": "will live",
        "correct_answer": "C",
        "explanation": "The present perfect is used for an action that began in the past and continues to the present."
    },

    {
        "topic": "Grammar",
        "subtopic": "Tenses",
        "difficulty": "Medium",
        "question": "If he had studied harder, he ____ the examination.",
        "option_a": "passes",
        "option_b": "will pass",
        "option_c": "would have passed",
        "option_d": "would pass",
        "correct_answer": "C",
        "explanation": "The third conditional uses 'would have' plus the past participle."
    },

    {
        "topic": "Grammar",
        "subtopic": "Concord",
        "difficulty": "Easy",
        "question": "Neither the teacher nor the students ____ aware of the change.",
        "option_a": "was",
        "option_b": "is",
        "option_c": "were",
        "option_d": "has",
        "correct_answer": "C",
        "explanation": "With 'neither...nor', the verb agrees with the nearer subject, 'students'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "The list of successful candidates ____ on the notice board.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "have",
        "option_d": "is",
        "correct_answer": "D",
        "explanation": "The subject is 'list', which is singular."
    },

    {
        "topic": "Grammar",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "Each of the boys ____ given a certificate.",
        "option_a": "were",
        "option_b": "was",
        "option_c": "have",
        "option_d": "are",
        "correct_answer": "B",
        "explanation": "'Each' is singular and takes a singular verb."
    },

    {
        "topic": "Grammar",
        "subtopic": "Concord",
        "difficulty": "Easy",
        "question": "The news ____ surprising.",
        "option_a": "were",
        "option_b": "are",
        "option_c": "was",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "'News' is treated as a singular uncountable noun."
    },

    {
        "topic": "Grammar",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "A number of students ____ absent today.",
        "option_a": "is",
        "option_b": "was",
        "option_c": "are",
        "option_d": "has",
        "correct_answer": "C",
        "explanation": "'A number of' takes a plural noun and plural verb."
    },

    {
        "topic": "Grammar",
        "subtopic": "Prepositions",
        "difficulty": "Easy",
        "question": "The students arrived ____ school early.",
        "option_a": "at",
        "option_b": "on",
        "option_c": "in",
        "option_d": "by",
        "correct_answer": "A",
        "explanation": "The standard expression is 'arrive at school'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Prepositions",
        "difficulty": "Medium",
        "question": "He has been absent ____ Monday.",
        "option_a": "for",
        "option_b": "since",
        "option_c": "from",
        "option_d": "by",
        "correct_answer": "B",
        "explanation": "'Since' is used with a specific starting point in time."
    },

    {
        "topic": "Grammar",
        "subtopic": "Prepositions",
        "difficulty": "Easy",
        "question": "The boy is good ____ Mathematics.",
        "option_a": "in",
        "option_b": "on",
        "option_c": "at",
        "option_d": "with",
        "correct_answer": "C",
        "explanation": "The correct expression is 'good at Mathematics'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Articles",
        "difficulty": "Easy",
        "question": "She bought ____ umbrella yesterday.",
        "option_a": "a",
        "option_b": "an",
        "option_c": "the",
        "option_d": "no article",
        "correct_answer": "B",
        "explanation": "'Umbrella' begins with a vowel sound, so 'an' is used."
    },

    {
        "topic": "Grammar",
        "subtopic": "Articles",
        "difficulty": "Medium",
        "question": "He is ____ honest man.",
        "option_a": "a",
        "option_b": "an",
        "option_c": "the",
        "option_d": "no article",
        "correct_answer": "B",
        "explanation": "'Honest' begins with a vowel sound because the 'h' is silent."
    },

    {
        "topic": "Grammar",
        "subtopic": "Pronouns",
        "difficulty": "Easy",
        "question": "This book belongs to James and ____.",
        "option_a": "I",
        "option_b": "me",
        "option_c": "my",
        "option_d": "mine",
        "correct_answer": "B",
        "explanation": "The pronoun follows the preposition 'to', so the object form 'me' is required."
    },

    {
        "topic": "Grammar",
        "subtopic": "Pronouns",
        "difficulty": "Medium",
        "question": "The principal asked Ada and ____ to remain behind.",
        "option_a": "I",
        "option_b": "me",
        "option_c": "my",
        "option_d": "mine",
        "correct_answer": "B",
        "explanation": "The pronoun is the object of 'asked', so 'me' is correct."
    },

    {
        "topic": "Grammar",
        "subtopic": "Adverbs",
        "difficulty": "Easy",
        "question": "The child answered the question ____.",
        "option_a": "correct",
        "option_b": "correctly",
        "option_c": "correctness",
        "option_d": "correcting",
        "correct_answer": "B",
        "explanation": "An adverb is required to modify the verb 'answered'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Adjectives",
        "difficulty": "Easy",
        "question": "The examination was ____ than we expected.",
        "option_a": "difficult",
        "option_b": "more difficult",
        "option_c": "most difficult",
        "option_d": "difficulty",
        "correct_answer": "B",
        "explanation": "The comparative form 'more difficult' is used when comparing two situations."
    },

    {
        "topic": "Grammar",
        "subtopic": "Question Tags",
        "difficulty": "Easy",
        "question": "You are coming with us, ____?",
        "option_a": "aren't you",
        "option_b": "are you",
        "option_c": "isn't it",
        "option_d": "don't you",
        "correct_answer": "A",
        "explanation": "A positive statement takes a negative question tag."
    },

    {
        "topic": "Grammar",
        "subtopic": "Question Tags",
        "difficulty": "Medium",
        "question": "He hardly visits us, ____?",
        "option_a": "doesn't he",
        "option_b": "does he",
        "option_c": "is he",
        "option_d": "didn't he",
        "correct_answer": "B",
        "explanation": "'Hardly' has a negative meaning, so the tag is positive."
    },

    {
        "topic": "Grammar",
        "subtopic": "Conditionals",
        "difficulty": "Medium",
        "question": "Unless you hurry, you ____ the bus.",
        "option_a": "missed",
        "option_b": "will miss",
        "option_c": "would miss",
        "option_d": "had missed",
        "correct_answer": "B",
        "explanation": "The first conditional uses a present condition and 'will' for the likely result."
    },


    # =====================================================
    # SYNONYMS
    # =====================================================

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Easy",
        "question": "Choose the option nearest in meaning to 'ABANDON'.",
        "option_a": "leave",
        "option_b": "collect",
        "option_c": "repair",
        "option_d": "protect",
        "correct_answer": "A",
        "explanation": "To abandon something means to leave it completely."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Easy",
        "question": "Choose the option nearest in meaning to 'BRIEF'.",
        "option_a": "long",
        "option_b": "short",
        "option_c": "heavy",
        "option_d": "wide",
        "correct_answer": "B",
        "explanation": "Brief means short in duration or length."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'DILIGENT'.",
        "option_a": "lazy",
        "option_b": "careless",
        "option_c": "hardworking",
        "option_d": "weak",
        "correct_answer": "C",
        "explanation": "A diligent person works carefully and consistently."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'HOSTILE'.",
        "option_a": "friendly",
        "option_b": "unfriendly",
        "option_c": "helpful",
        "option_d": "peaceful",
        "correct_answer": "B",
        "explanation": "Hostile means unfriendly or antagonistic."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'OBSOLETE'.",
        "option_a": "modern",
        "option_b": "expensive",
        "option_c": "outdated",
        "option_d": "valuable",
        "correct_answer": "C",
        "explanation": "Obsolete means no longer useful or current."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Easy",
        "question": "Choose the option nearest in meaning to 'GENEROUS'.",
        "option_a": "kind-hearted",
        "option_b": "selfish",
        "option_c": "angry",
        "option_d": "strict",
        "correct_answer": "A",
        "explanation": "A generous person is willing to give or share."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'IMPEDE'.",
        "option_a": "assist",
        "option_b": "delay",
        "option_c": "encourage",
        "option_d": "complete",
        "correct_answer": "B",
        "explanation": "To impede means to hinder or delay."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'PRUDENT'.",
        "option_a": "careful",
        "option_b": "reckless",
        "option_c": "careless",
        "option_d": "noisy",
        "correct_answer": "A",
        "explanation": "Prudent means showing good judgment and care."
    },


    # =====================================================
    # ANTONYMS
    # =====================================================

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the option opposite in meaning to 'ANCIENT'.",
        "option_a": "old",
        "option_b": "modern",
        "option_c": "historic",
        "option_d": "traditional",
        "correct_answer": "B",
        "explanation": "Modern is opposite in meaning to ancient."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the option opposite in meaning to 'VICTORY'.",
        "option_a": "success",
        "option_b": "triumph",
        "option_c": "defeat",
        "option_d": "achievement",
        "correct_answer": "C",
        "explanation": "Defeat is the opposite of victory."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the option opposite in meaning to 'EXPAND'.",
        "option_a": "increase",
        "option_b": "enlarge",
        "option_c": "contract",
        "option_d": "develop",
        "correct_answer": "C",
        "explanation": "To contract means to become smaller."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the option opposite in meaning to 'OPTIMISTIC'.",
        "option_a": "hopeful",
        "option_b": "positive",
        "option_c": "pessimistic",
        "option_d": "confident",
        "correct_answer": "C",
        "explanation": "Pessimistic is the opposite of optimistic."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the option opposite in meaning to 'TRANSPARENT'.",
        "option_a": "clear",
        "option_b": "obvious",
        "option_c": "opaque",
        "option_d": "visible",
        "correct_answer": "C",
        "explanation": "Opaque means not allowing light to pass through."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the option opposite in meaning to 'PERMANENT'.",
        "option_a": "lasting",
        "option_b": "temporary",
        "option_c": "fixed",
        "option_d": "stable",
        "correct_answer": "B",
        "explanation": "Temporary means lasting only for a limited time."
    },


    # =====================================================
    # IDIOMS / EXPRESSIONS
    # =====================================================

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Easy",
        "question": "If someone 'breaks the ice', what does the person do?",
        "option_a": "start a friendly conversation",
        "option_b": "destroy something",
        "option_c": "become angry",
        "option_d": "leave immediately",
        "correct_answer": "A",
        "explanation": "To break the ice means to make people feel more comfortable."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "If a student 'hits the nail on the head', the student has ____.",
        "option_a": "made a mistake",
        "option_b": "said exactly the right thing",
        "option_c": "become confused",
        "option_d": "worked slowly",
        "correct_answer": "B",
        "explanation": "The expression means to describe or identify something exactly."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Easy",
        "question": "To 'see eye to eye' with someone means to ____.",
        "option_a": "fight with the person",
        "option_b": "agree with the person",
        "option_c": "avoid the person",
        "option_d": "watch the person",
        "correct_answer": "B",
        "explanation": "To see eye to eye means to agree."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "If a person is 'under the weather', the person is ____.",
        "option_a": "very happy",
        "option_b": "slightly ill",
        "option_c": "outside",
        "option_d": "wealthy",
        "correct_answer": "B",
        "explanation": "The expression means to feel unwell."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "When someone 'spills the beans', the person ____.",
        "option_a": "cooks food",
        "option_b": "reveals a secret",
        "option_c": "starts a business",
        "option_d": "makes a promise",
        "correct_answer": "B",
        "explanation": "To spill the beans means to reveal secret information."
    },


    # =====================================================
    # SENTENCE COMPLETION
    # =====================================================

    {
        "topic": "Sentence Completion",
        "subtopic": "Word Choice",
        "difficulty": "Easy",
        "question": "The principal advised the students to ____ attention in class.",
        "option_a": "make",
        "option_b": "pay",
        "option_c": "give",
        "option_d": "do",
        "correct_answer": "B",
        "explanation": "The correct expression is 'pay attention'."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Word Choice",
        "difficulty": "Easy",
        "question": "The police are investigating the ____ of the missing student.",
        "option_a": "disappearance",
        "option_b": "appearance",
        "option_c": "arrival",
        "option_d": "entrance",
        "correct_answer": "A",
        "explanation": "Disappearance refers to the act of becoming missing."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Word Choice",
        "difficulty": "Medium",
        "question": "The manager asked the workers to ____ the meeting until Monday.",
        "option_a": "postpone",
        "option_b": "prevent",
        "option_c": "cancelled",
        "option_d": "refuse",
        "correct_answer": "A",
        "explanation": "To postpone means to delay something until a later time."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Word Choice",
        "difficulty": "Medium",
        "question": "The witness gave a ____ account of what happened.",
        "option_a": "detailed",
        "option_b": "detail",
        "option_c": "detailing",
        "option_d": "details",
        "correct_answer": "A",
        "explanation": "'Detailed' is the adjective required to describe 'account'."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Word Choice",
        "difficulty": "Easy",
        "question": "The doctor advised him to ____ smoking.",
        "option_a": "give up",
        "option_b": "give in",
        "option_c": "give out",
        "option_d": "give away",
        "correct_answer": "A",
        "explanation": "'Give up' means to stop doing something."
    },


    # =====================================================
    # PHRASAL VERBS
    # =====================================================

    {
        "topic": "Vocabulary",
        "subtopic": "Phrasal Verbs",
        "difficulty": "Easy",
        "question": "The meeting was ____ because the chairman was absent.",
        "option_a": "called off",
        "option_b": "called in",
        "option_c": "called up",
        "option_d": "called over",
        "correct_answer": "A",
        "explanation": "'Called off' means cancelled."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Phrasal Verbs",
        "difficulty": "Medium",
        "question": "The student ____ the meaning of the unfamiliar word.",
        "option_a": "looked after",
        "option_b": "looked up",
        "option_c": "looked into",
        "option_d": "looked over",
        "correct_answer": "B",
        "explanation": "'Look up' means to search for information."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Phrasal Verbs",
        "difficulty": "Medium",
        "question": "The committee will ____ the matter carefully.",
        "option_a": "look into",
        "option_b": "look after",
        "option_c": "look away",
        "option_d": "look out",
        "correct_answer": "A",
        "explanation": "'Look into' means to investigate."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Phrasal Verbs",
        "difficulty": "Easy",
        "question": "Please ____ the lights before leaving the room.",
        "option_a": "turn on",
        "option_b": "turn up",
        "option_c": "turn off",
        "option_d": "turn into",
        "correct_answer": "C",
        "explanation": "'Turn off' means to switch something off."
    },


    # =====================================================
    # WORD RELATIONSHIPS
    # =====================================================

    {
        "topic": "Vocabulary",
        "subtopic": "Word Relationships",
        "difficulty": "Easy",
        "question": "Choose the word that best completes the relationship: Doctor : Hospital :: Teacher : ____",
        "option_a": "market",
        "option_b": "school",
        "option_c": "court",
        "option_d": "farm",
        "correct_answer": "B",
        "explanation": "A doctor commonly works in a hospital; a teacher commonly works in a school."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Relationships",
        "difficulty": "Easy",
        "question": "Choose the word that best completes the relationship: Bird : Nest :: Lion : ____",
        "option_a": "den",
        "option_b": "web",
        "option_c": "stable",
        "option_d": "hive",
        "correct_answer": "A",
        "explanation": "A bird lives in a nest; a lion commonly lives in a den."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Relationships",
        "difficulty": "Medium",
        "question": "Choose the word that best completes the relationship: Pen : Write :: Knife : ____",
        "option_a": "cut",
        "option_b": "read",
        "option_c": "draw",
        "option_d": "speak",
        "correct_answer": "A",
        "explanation": "A pen is used for writing; a knife is used for cutting."
    },


    # =====================================================
    # PARTS OF SPEECH
    # =====================================================

    {
        "topic": "Grammar",
        "subtopic": "Parts of Speech",
        "difficulty": "Easy",
        "question": "In the sentence 'The boy ran quickly', what part of speech is 'quickly'?",
        "option_a": "Noun",
        "option_b": "Verb",
        "option_c": "Adjective",
        "option_d": "Adverb",
        "correct_answer": "D",
        "explanation": "'Quickly' modifies the verb 'ran', so it is an adverb."
    },

    {
        "topic": "Grammar",
        "subtopic": "Parts of Speech",
        "difficulty": "Easy",
        "question": "In the sentence 'The beautiful girl smiled', what part of speech is 'beautiful'?",
        "option_a": "Adjective",
        "option_b": "Adverb",
        "option_c": "Verb",
        "option_d": "Preposition",
        "correct_answer": "A",
        "explanation": "'Beautiful' describes the noun 'girl', making it an adjective."
    },

    {
        "topic": "Grammar",
        "subtopic": "Parts of Speech",
        "difficulty": "Medium",
        "question": "In the sentence 'They arrived after lunch', what part of speech is 'after'?",
        "option_a": "Noun",
        "option_b": "Preposition",
        "option_c": "Adjective",
        "option_d": "Pronoun",
        "correct_answer": "B",
        "explanation": "'After' shows the relationship between 'arrived' and 'lunch'."
    },


    # =====================================================
    # SENTENCE STRUCTURE
    # =====================================================

    {
        "topic": "Grammar",
        "subtopic": "Sentence Structure",
        "difficulty": "Easy",
        "question": "Which sentence is correctly written?",
        "option_a": "She don't like rice.",
        "option_b": "She doesn't likes rice.",
        "option_c": "She doesn't like rice.",
        "option_d": "She not like rice.",
        "correct_answer": "C",
        "explanation": "After 'doesn't', the main verb remains in its base form."
    },

    {
        "topic": "Grammar",
        "subtopic": "Sentence Structure",
        "difficulty": "Medium",
        "question": "Which sentence is grammatically correct?",
        "option_a": "Neither of the boys are ready.",
        "option_b": "Neither of the boys is ready.",
        "option_c": "Neither of the boys were ready.",
        "option_d": "Neither boys is ready.",
        "correct_answer": "B",
        "explanation": "'Neither' is singular and takes 'is' in formal standard English."
    },

    {
        "topic": "Grammar",
        "subtopic": "Sentence Structure",
        "difficulty": "Medium",
        "question": "Which sentence is correctly written?",
        "option_a": "Despite of the rain, we went out.",
        "option_b": "Despite the rain, we went out.",
        "option_c": "Despite from the rain, we went out.",
        "option_d": "Despite to the rain, we went out.",
        "correct_answer": "B",
        "explanation": "'Despite' is not followed by 'of'."
    },


    # =====================================================
    # VOCABULARY IN CONTEXT
    # =====================================================

    {
        "topic": "Vocabulary",
        "subtopic": "Contextual Meaning",
        "difficulty": "Medium",
        "question": "The politician gave an evasive answer. This means that the answer was ____.",
        "option_a": "direct",
        "option_b": "clear",
        "option_c": "avoiding the main point",
        "option_d": "accurate",
        "correct_answer": "C",
        "explanation": "An evasive response avoids giving a direct answer."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Contextual Meaning",
        "difficulty": "Medium",
        "question": "The teacher reprimanded the student for cheating. 'Reprimanded' means ____.",
        "option_a": "praised",
        "option_b": "criticized",
        "option_c": "rewarded",
        "option_d": "ignored",
        "correct_answer": "B",
        "explanation": "To reprimand means to express strong disapproval."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Contextual Meaning",
        "difficulty": "Medium",
        "question": "The manager was reluctant to approve the proposal. 'Reluctant' means ____.",
        "option_a": "eager",
        "option_b": "unwilling",
        "option_c": "excited",
        "option_d": "certain",
        "correct_answer": "B",
        "explanation": "Reluctant means unwilling or hesitant."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Contextual Meaning",
        "difficulty": "Medium",
        "question": "The evidence was conclusive. This means that it was ____.",
        "option_a": "uncertain",
        "option_b": "confusing",
        "option_c": "decisive",
        "option_d": "irrelevant",
        "correct_answer": "C",
        "explanation": "Conclusive evidence provides a decisive result."
    },


    # =====================================================
    # MORE GRAMMAR
    # =====================================================

    {
        "topic": "Grammar",
        "subtopic": "Active and Passive Voice",
        "difficulty": "Medium",
        "question": "The mechanic repaired the car. Which is the correct passive form?",
        "option_a": "The car repaired the mechanic.",
        "option_b": "The car was repaired by the mechanic.",
        "option_c": "The car is repaired by the mechanic yesterday.",
        "option_d": "The mechanic was repaired by the car.",
        "correct_answer": "B",
        "explanation": "The object 'car' becomes the subject in the passive construction."
    },

    {
        "topic": "Grammar",
        "subtopic": "Active and Passive Voice",
        "difficulty": "Medium",
        "question": "The students completed the assignment. The passive form is ____.",
        "option_a": "The assignment completed the students.",
        "option_b": "The assignment was completed by the students.",
        "option_c": "The assignment is completing the students.",
        "option_d": "The students were completed by the assignment.",
        "correct_answer": "B",
        "explanation": "The simple past passive is formed with 'was/were + past participle'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Reported Speech",
        "difficulty": "Medium",
        "question": "Tunde said, 'I am tired.' The reported form is ____.",
        "option_a": "Tunde said that I am tired.",
        "option_b": "Tunde said that he was tired.",
        "option_c": "Tunde said that he is tired yesterday.",
        "option_d": "Tunde says that he was tired.",
        "correct_answer": "B",
        "explanation": "In reported speech, 'I am' changes to 'he was' when reporting a past statement."
    },

    {
        "topic": "Grammar",
        "subtopic": "Reported Speech",
        "difficulty": "Medium",
        "question": "Ngozi said, 'I will come tomorrow.' The reported form is ____.",
        "option_a": "Ngozi said that she would come the following day.",
        "option_b": "Ngozi said that she will come yesterday.",
        "option_c": "Ngozi said that I would come tomorrow.",
        "option_d": "Ngozi says that she came tomorrow.",
        "correct_answer": "A",
        "explanation": "In reported speech, 'will' changes to 'would' and 'tomorrow' changes according to the reporting time."
    },


    # =====================================================
    # MORE SYNONYMS
    # =====================================================

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'METICULOUS'.",
        "option_a": "careless",
        "option_b": "very careful",
        "option_c": "quick",
        "option_d": "lazy",
        "correct_answer": "B",
        "explanation": "Meticulous means extremely careful and precise."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'AMBIGUOUS'.",
        "option_a": "unclear",
        "option_b": "obvious",
        "option_c": "simple",
        "option_d": "certain",
        "correct_answer": "A",
        "explanation": "Ambiguous means open to more than one interpretation."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'VITAL'.",
        "option_a": "unnecessary",
        "option_b": "essential",
        "option_c": "ordinary",
        "option_d": "minor",
        "correct_answer": "B",
        "explanation": "Vital means extremely important or necessary."
    },


    # =====================================================
    # MORE ANTONYMS
    # =====================================================

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the option opposite in meaning to 'SCARCE'.",
        "option_a": "rare",
        "option_b": "limited",
        "option_c": "abundant",
        "option_d": "insufficient",
        "correct_answer": "C",
        "explanation": "Abundant means available in large quantities."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the option opposite in meaning to 'RELUCTANT'.",
        "option_a": "hesitant",
        "option_b": "unwilling",
        "option_c": "eager",
        "option_d": "doubtful",
        "correct_answer": "C",
        "explanation": "Eager means enthusiastic or willing."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the option opposite in meaning to 'FREQUENT'.",
        "option_a": "regular",
        "option_b": "rare",
        "option_c": "common",
        "option_d": "usual",
        "correct_answer": "B",
        "explanation": "Rare means occurring infrequently."
    },


    # =====================================================
    # ORAL ENGLISH
    # =====================================================

    {
        "topic": "Oral English",
        "subtopic": "Vowel Sounds",
        "difficulty": "Medium",
        "question": "Which word has the same vowel sound as the vowel sound in 'seat'?",
        "option_a": "sit",
        "option_b": "beat",
        "option_c": "set",
        "option_d": "said",
        "correct_answer": "B",
        "explanation": "'Seat' and 'beat' contain the long /iː/ vowel sound."
    },

    {
        "topic": "Oral English",
        "subtopic": "Vowel Sounds",
        "difficulty": "Medium",
        "question": "Which word has the same vowel sound as the vowel sound in 'food'?",
        "option_a": "good",
        "option_b": "flood",
        "option_c": "mood",
        "option_d": "blood",
        "correct_answer": "C",
        "explanation": "'Food' and 'mood' contain the /uː/ vowel sound."
    },

    {
        "topic": "Oral English",
        "subtopic": "Consonant Sounds",
        "difficulty": "Medium",
        "question": "Which word begins with the same consonant sound as 'chair'?",
        "option_a": "share",
        "option_b": "cheese",
        "option_c": "gear",
        "option_d": "there",
        "correct_answer": "B",
        "explanation": "'Chair' and 'cheese' begin with the /tʃ/ sound."
    },

    {
        "topic": "Oral English",
        "subtopic": "Consonant Sounds",
        "difficulty": "Medium",
        "question": "Which word begins with the same consonant sound as 'judge'?",
        "option_a": "giant",
        "option_b": "yellow",
        "option_c": "church",
        "option_d": "school",
        "correct_answer": "A",
        "explanation": "'Judge' and 'giant' begin with the /dʒ/ sound."
    },


    # =====================================================
    # COMPREHENSION-STYLE QUESTIONS
    # =====================================================

    {
        "topic": "Comprehension",
        "subtopic": "Main Idea",
        "difficulty": "Medium",
        "question": "A paragraph explains how regular exercise improves concentration, strengthens the body and reduces stress. What is the main idea?",
        "option_a": "Exercise is only useful for athletes.",
        "option_b": "Regular exercise has several benefits.",
        "option_c": "Students should avoid exercise.",
        "option_d": "Stress is caused only by school.",
        "correct_answer": "B",
        "explanation": "The paragraph presents several benefits of regular exercise."
    },

    {
        "topic": "Comprehension",
        "subtopic": "Inference",
        "difficulty": "Medium",
        "question": "A student consistently arrives early, completes assignments and studies before examinations. What can reasonably be inferred?",
        "option_a": "The student dislikes school.",
        "option_b": "The student is disciplined.",
        "option_c": "The student never studies.",
        "option_d": "The student is careless.",
        "correct_answer": "B",
        "explanation": "The student's behaviour suggests discipline and good preparation."
    },

    {
        "topic": "Comprehension",
        "subtopic": "Vocabulary in Context",
        "difficulty": "Medium",
        "question": "The road was impassable after the heavy rainfall. The word 'impassable' means ____.",
        "option_a": "easy to use",
        "option_b": "difficult or impossible to travel on",
        "option_c": "newly constructed",
        "option_d": "very beautiful",
        "correct_answer": "B",
        "explanation": "An impassable road cannot be travelled through easily or at all."
    },


    # =====================================================
    # CLOZE-STYLE QUESTIONS
    # =====================================================

    {
        "topic": "Cloze Test",
        "subtopic": "Vocabulary",
        "difficulty": "Easy",
        "question": "The students were excited because their teacher had ____ them that the examination would be postponed.",
        "option_a": "told",
        "option_b": "said",
        "option_c": "spoken",
        "option_d": "talked",
        "correct_answer": "A",
        "explanation": "The correct construction is 'told them'."
    },

    {
        "topic": "Cloze Test",
        "subtopic": "Grammar",
        "difficulty": "Medium",
        "question": "Although he was tired, he continued ____ until he completed the work.",
        "option_a": "work",
        "option_b": "worked",
        "option_c": "working",
        "option_d": "works",
        "correct_answer": "C",
        "explanation": "The expression 'continued working' is grammatically correct."
    },

    {
        "topic": "Cloze Test",
        "subtopic": "Prepositions",
        "difficulty": "Medium",
        "question": "The principal congratulated the students ____ their excellent performance.",
        "option_a": "for",
        "option_b": "on",
        "option_c": "at",
        "option_d": "with",
        "correct_answer": "B",
        "explanation": "The correct expression is 'congratulated someone on something'."
    },


    # =====================================================
    # MORE MIXED QUESTIONS
    # =====================================================

    {
        "topic": "Grammar",
        "subtopic": "Gerunds",
        "difficulty": "Medium",
        "question": "She enjoys ____ novels in her spare time.",
        "option_a": "read",
        "option_b": "reads",
        "option_c": "reading",
        "option_d": "to reading",
        "correct_answer": "C",
        "explanation": "The verb 'enjoy' is followed by a gerund."
    },

    {
        "topic": "Grammar",
        "subtopic": "Infinitives",
        "difficulty": "Medium",
        "question": "The student decided ____ harder for the next examination.",
        "option_a": "study",
        "option_b": "studying",
        "option_c": "to study",
        "option_d": "studied",
        "correct_answer": "C",
        "explanation": "'Decide' is normally followed by an infinitive."
    },

    {
        "topic": "Grammar",
        "subtopic": "Modal Verbs",
        "difficulty": "Easy",
        "question": "You ____ obey the rules of the examination hall.",
        "option_a": "must",
        "option_b": "might",
        "option_c": "could",
        "option_d": "would",
        "correct_answer": "A",
        "explanation": "'Must' expresses strong obligation."
    },

    {
        "topic": "Grammar",
        "subtopic": "Modal Verbs",
        "difficulty": "Medium",
        "question": "You ____ have informed me earlier.",
        "option_a": "should",
        "option_b": "should have",
        "option_c": "must",
        "option_d": "can",
        "correct_answer": "B",
        "explanation": "'Should have' expresses something that was advisable but did not happen."
    },

    {
        "topic": "Grammar",
        "subtopic": "Relative Clauses",
        "difficulty": "Medium",
        "question": "The man ____ won the award is my uncle.",
        "option_a": "which",
        "option_b": "whose",
        "option_c": "who",
        "option_d": "whom",
        "correct_answer": "C",
        "explanation": "'Who' is used as the relative pronoun referring to a person acting as the subject."
    },

    {
        "topic": "Grammar",
        "subtopic": "Relative Clauses",
        "difficulty": "Medium",
        "question": "The book ____ I borrowed was very interesting.",
        "option_a": "who",
        "option_b": "which",
        "option_c": "whose",
        "option_d": "whom",
        "correct_answer": "B",
        "explanation": "'Which' refers to the thing 'book'."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Easy",
        "question": "Choose the option nearest in meaning to 'RAPID'.",
        "option_a": "slow",
        "option_b": "fast",
        "option_c": "weak",
        "option_d": "late",
        "correct_answer": "B",
        "explanation": "Rapid means fast or quick."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'COMMENCE'.",
        "option_a": "finish",
        "option_b": "begin",
        "option_c": "stop",
        "option_d": "delay",
        "correct_answer": "B",
        "explanation": "Commence means begin."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the option opposite in meaning to 'ACCEPT'.",
        "option_a": "receive",
        "option_b": "approve",
        "option_c": "reject",
        "option_d": "allow",
        "correct_answer": "C",
        "explanation": "Reject is opposite in meaning to accept."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the option opposite in meaning to 'GENUINE'.",
        "option_a": "real",
        "option_b": "authentic",
        "option_c": "false",
        "option_d": "original",
        "correct_answer": "C",
        "explanation": "False is opposite in meaning to genuine."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "To 'cut corners' means to ____.",
        "option_a": "take unnecessary risks",
        "option_b": "do something cheaply or carelessly",
        "option_c": "cut a piece of paper",
        "option_d": "arrive early",
        "correct_answer": "B",
        "explanation": "The expression means to take shortcuts, often at the expense of quality."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "If someone 'keeps an eye on' something, the person ____.",
        "option_a": "ignores it",
        "option_b": "watches it carefully",
        "option_c": "destroys it",
        "option_d": "moves it",
        "correct_answer": "B",
        "explanation": "To keep an eye on something means to watch or monitor it."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Collocations",
        "difficulty": "Easy",
        "question": "The athlete made ____ progress after months of training.",
        "option_a": "much",
        "option_b": "many",
        "option_c": "several",
        "option_d": "a few",
        "correct_answer": "A",
        "explanation": "'Progress' is generally treated as an uncountable noun, so 'much' is appropriate."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Collocations",
        "difficulty": "Medium",
        "question": "The government should take ____ measures to reduce traffic congestion.",
        "option_a": "effective",
        "option_b": "effect",
        "option_c": "effectively",
        "option_d": "effectiveness",
        "correct_answer": "A",
        "explanation": "'Effective' is the adjective that appropriately describes 'measures'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Countable and Uncountable Nouns",
        "difficulty": "Easy",
        "question": "We need some ____ before making a decision.",
        "option_a": "informations",
        "option_b": "information",
        "option_c": "an information",
        "option_d": "inform",
        "correct_answer": "B",
        "explanation": "'Information' is an uncountable noun."
    },

    {
        "topic": "Grammar",
        "subtopic": "Countable and Uncountable Nouns",
        "difficulty": "Easy",
        "question": "She gave me two useful ____.",
        "option_a": "advices",
        "option_b": "advice",
        "option_c": "pieces of advice",
        "option_d": "advise",
        "correct_answer": "C",
        "explanation": "'Advice' is uncountable, so 'two pieces of advice' is correct."
    },

    {
        "topic": "Grammar",
        "subtopic": "Comparison",
        "difficulty": "Easy",
        "question": "Of the three students, Ada is the ____.",
        "option_a": "tall",
        "option_b": "taller",
        "option_c": "tallest",
        "option_d": "more tall",
        "correct_answer": "C",
        "explanation": "The superlative form is used when comparing three or more people."
    },

    {
        "topic": "Grammar",
        "subtopic": "Comparison",
        "difficulty": "Medium",
        "question": "This problem is ____ than the previous one.",
        "option_a": "complex",
        "option_b": "more complex",
        "option_c": "most complex",
        "option_d": "complexest",
        "correct_answer": "B",
        "explanation": "'More complex' is the correct comparative form."
    },

    {
        "topic": "Grammar",
        "subtopic": "Negatives",
        "difficulty": "Medium",
        "question": "Hardly ____ the examination begun when the lights went off.",
        "option_a": "had",
        "option_b": "has",
        "option_c": "did",
        "option_d": "was",
        "correct_answer": "A",
        "explanation": "The structure is 'Hardly had...when...' for two closely connected past events."
    },

    {
        "topic": "Grammar",
        "subtopic": "Inversion",
        "difficulty": "Hard",
        "question": "Not only ____ intelligent, but she is also hardworking.",
        "option_a": "she is",
        "option_b": "is she",
        "option_c": "she was",
        "option_d": "was she",
        "correct_answer": "B",
        "explanation": "After 'not only' at the beginning, subject-verb inversion is used."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Meaning",
        "difficulty": "Medium",
        "question": "A person who is 'compassionate' is one who is ____.",
        "option_a": "cruel",
        "option_b": "sympathetic",
        "option_c": "selfish",
        "option_d": "careless",
        "correct_answer": "B",
        "explanation": "A compassionate person shows sympathy and concern for others."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Meaning",
        "difficulty": "Medium",
        "question": "A 'versatile' person is someone who ____.",
        "option_a": "can perform many different tasks",
        "option_b": "refuses to learn",
        "option_c": "is always angry",
        "option_d": "works only at night",
        "correct_answer": "A",
        "explanation": "Versatile describes someone capable of adapting to or doing many different things."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Meaning",
        "difficulty": "Medium",
        "question": "If a plan is 'feasible', it is ____.",
        "option_a": "impossible",
        "option_b": "practical and possible",
        "option_c": "illegal",
        "option_d": "unnecessary",
        "correct_answer": "B",
        "explanation": "Feasible means possible and practical."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Meaning",
        "difficulty": "Medium",
        "question": "A 'benevolent' person is ____.",
        "option_a": "kind and generous",
        "option_b": "violent",
        "option_c": "dishonest",
        "option_d": "careless",
        "correct_answer": "A",
        "explanation": "Benevolent means kind-hearted and well-meaning."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Meaning",
        "difficulty": "Medium",
        "question": "A 'credible' explanation is one that is ____.",
        "option_a": "believable",
        "option_b": "impossible",
        "option_c": "confusing",
        "option_d": "irrelevant",
        "correct_answer": "A",
        "explanation": "Credible means believable or trustworthy."
    },

    {
        "topic": "Oral English",
        "subtopic": "Stress",
        "difficulty": "Medium",
        "question": "Which word has stress on the second syllable?",
        "option_a": "TAble",
        "option_b": "DOCtor",
        "option_c": "reLAX",
        "option_d": "WINdow",
        "correct_answer": "C",
        "explanation": "The main stress in 'relax' falls on the second syllable."
    },

    {
        "topic": "Oral English",
        "subtopic": "Rhyming Words",
        "difficulty": "Easy",
        "question": "Which word rhymes with 'light'?",
        "option_a": "late",
        "option_b": "might",
        "option_c": "let",
        "option_d": "lot",
        "correct_answer": "B",
        "explanation": "'Light' and 'might' have the same final sound."
    },

    {
        "topic": "Grammar",
        "subtopic": "Conjunctions",
        "difficulty": "Easy",
        "question": "I wanted to attend the programme, ____ I was ill.",
        "option_a": "because",
        "option_b": "but",
        "option_c": "so",
        "option_d": "and",
        "correct_answer": "B",
        "explanation": "'But' expresses the contrast between wanting to attend and being ill."
    },

    {
        "topic": "Grammar",
        "subtopic": "Conjunctions",
        "difficulty": "Easy",
        "question": "He stayed at home ____ it was raining heavily.",
        "option_a": "because",
        "option_b": "although",
        "option_c": "unless",
        "option_d": "while",
        "correct_answer": "A",
        "explanation": "'Because' introduces the reason he stayed at home."
    },

    {
        "topic": "Grammar",
        "subtopic": "Conjunctions",
        "difficulty": "Medium",
        "question": "____ he was tired, he continued working.",
        "option_a": "Because",
        "option_b": "Although",
        "option_c": "So",
        "option_d": "And",
        "correct_answer": "B",
        "explanation": "'Although' introduces a contrast."
    },

    {
        "topic": "Grammar",
        "subtopic": "Punctuation",
        "difficulty": "Easy",
        "question": "Which sentence is correctly punctuated?",
        "option_a": "However I decided to stay.",
        "option_b": "However, I decided to stay.",
        "option_c": "However I, decided to stay.",
        "option_d": "However, I, decided to stay.",
        "correct_answer": "B",
        "explanation": "A comma normally follows an introductory 'However'."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'HOST'.",
        "option_a": "entertain",
        "option_b": "reject",
        "option_c": "avoid",
        "option_d": "remove",
        "correct_answer": "A",
        "explanation": "As a verb, 'host' can mean to receive or entertain guests."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the option opposite in meaning to 'COMPLICATED'.",
        "option_a": "difficult",
        "option_b": "simple",
        "option_c": "confusing",
        "option_d": "complex",
        "correct_answer": "B",
        "explanation": "Simple is opposite in meaning to complicated."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "To 'be in hot water' means to be ____.",
        "option_a": "comfortable",
        "option_b": "in trouble",
        "option_c": "very wealthy",
        "option_d": "very relaxed",
        "correct_answer": "B",
        "explanation": "The expression means to be in difficulty or trouble."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "To 'call it a day' means to ____.",
        "option_a": "start working",
        "option_b": "stop working for the day",
        "option_c": "change the date",
        "option_d": "make a phone call",
        "correct_answer": "B",
        "explanation": "The expression means to stop work for the day."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Word Choice",
        "difficulty": "Medium",
        "question": "The new policy will come ____ effect next month.",
        "option_a": "to",
        "option_b": "into",
        "option_c": "in",
        "option_d": "at",
        "correct_answer": "B",
        "explanation": "The correct expression is 'come into effect'."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Word Choice",
        "difficulty": "Medium",
        "question": "The student is capable ____ solving the problem.",
        "option_a": "to",
        "option_b": "of",
        "option_c": "for",
        "option_d": "with",
        "correct_answer": "B",
        "explanation": "The correct construction is 'capable of'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Agreement",
        "difficulty": "Medium",
        "question": "Ten kilometres ____ a long distance to walk.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "A distance considered as one unit takes a singular verb."
    },

    {
        "topic": "Grammar",
        "subtopic": "Agreement",
        "difficulty": "Medium",
        "question": "The furniture in the room ____ very expensive.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "'Furniture' is an uncountable singular noun."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Contextual Meaning",
        "difficulty": "Hard",
        "question": "The chairman's speech was succinct. This means it was ____.",
        "option_a": "very lengthy",
        "option_b": "brief and clear",
        "option_c": "confusing",
        "option_d": "angry",
        "correct_answer": "B",
        "explanation": "Succinct means expressed clearly and briefly."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Contextual Meaning",
        "difficulty": "Hard",
        "question": "The student's argument was coherent. This means it was ____.",
        "option_a": "logical and connected",
        "option_b": "completely false",
        "option_c": "very short",
        "option_d": "unrelated",
        "correct_answer": "A",
        "explanation": "A coherent argument is logical and well connected."
    },

    {
        "topic": "Grammar",
        "subtopic": "Sentence Transformation",
        "difficulty": "Medium",
        "question": "No other student in the class is as tall as John. This means John is ____.",
        "option_a": "taller than every student",
        "option_b": "the tallest student in the class",
        "option_c": "shorter than every student",
        "option_d": "one of the shortest students",
        "correct_answer": "B",
        "explanation": "The statement establishes John as the tallest student."
    },

    {
        "topic": "Grammar",
        "subtopic": "Sentence Transformation",
        "difficulty": "Medium",
        "question": "Despite being tired, she completed the assignment. This means ____.",
        "option_a": "She was tired, but she completed the assignment.",
        "option_b": "She did not complete the assignment.",
        "option_c": "She was not tired.",
        "option_d": "She completed the assignment because she was tired.",
        "correct_answer": "A",
        "explanation": "'Despite' introduces a contrast."
    },

    {
        "topic": "Grammar",
        "subtopic": "Conditional Sentences",
        "difficulty": "Medium",
        "question": "If I were you, I ____ apologize.",
        "option_a": "will",
        "option_b": "would",
        "option_c": "shall",
        "option_d": "can",
        "correct_answer": "B",
        "explanation": "The second conditional uses 'would' for an imaginary situation."
    },

    {
        "topic": "Grammar",
        "subtopic": "Conditional Sentences",
        "difficulty": "Medium",
        "question": "If it rains tomorrow, we ____ at home.",
        "option_a": "stay",
        "option_b": "stayed",
        "option_c": "will stay",
        "option_d": "would stayed",
        "correct_answer": "C",
        "explanation": "The first conditional uses 'will' in the main clause."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Hard",
        "question": "Choose the option nearest in meaning to 'ELUSIVE'.",
        "option_a": "easy to find",
        "option_b": "difficult to find or understand",
        "option_c": "very expensive",
        "option_d": "extremely large",
        "correct_answer": "B",
        "explanation": "Elusive describes something difficult to find, catch or understand."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Hard",
        "question": "Choose the option opposite in meaning to 'HOSTILE'.",
        "option_a": "aggressive",
        "option_b": "friendly",
        "option_c": "violent",
        "option_d": "angry",
        "correct_answer": "B",
        "explanation": "Friendly is opposite in meaning to hostile."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "If someone 'goes the extra mile', the person ____.",
        "option_a": "travels abroad",
        "option_b": "makes an additional effort",
        "option_c": "gets lost",
        "option_d": "refuses to work",
        "correct_answer": "B",
        "explanation": "The expression means to make more effort than is normally expected."
    },

    {
        "topic": "Grammar",
        "subtopic": "Subject-Verb Agreement",
        "difficulty": "Medium",
        "question": "Either the teachers or the principal ____ responsible for the decision.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "The verb agrees with the nearer singular subject, 'principal'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Subject-Verb Agreement",
        "difficulty": "Medium",
        "question": "The quality of these products ____ improved considerably.",
        "option_a": "have",
        "option_b": "has",
        "option_c": "are",
        "option_d": "were",
        "correct_answer": "B",
        "explanation": "The subject is 'quality', which is singular."
    },

    {
        "topic": "Grammar",
        "subtopic": "Prepositions",
        "difficulty": "Medium",
        "question": "She is interested ____ studying engineering.",
        "option_a": "on",
        "option_b": "at",
        "option_c": "in",
        "option_d": "for",
        "correct_answer": "C",
        "explanation": "The correct expression is 'interested in'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Prepositions",
        "difficulty": "Medium",
        "question": "He apologized ____ being late.",
        "option_a": "for",
        "option_b": "of",
        "option_c": "on",
        "option_d": "at",
        "correct_answer": "A",
        "explanation": "The correct expression is 'apologized for'."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Easy",
        "question": "Choose the option nearest in meaning to 'ENORMOUS'.",
        "option_a": "tiny",
        "option_b": "huge",
        "option_c": "weak",
        "option_d": "narrow",
        "correct_answer": "B",
        "explanation": "Enormous means extremely large."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Easy",
        "question": "Choose the option opposite in meaning to 'ARRIVE'.",
        "option_a": "come",
        "option_b": "reach",
        "option_c": "depart",
        "option_d": "enter",
        "correct_answer": "C",
        "explanation": "Depart means to leave."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Collocations",
        "difficulty": "Medium",
        "question": "The company is responsible ____ providing the equipment.",
        "option_a": "of",
        "option_b": "for",
        "option_c": "with",
        "option_d": "on",
        "correct_answer": "B",
        "explanation": "The correct expression is 'responsible for'."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Collocations",
        "difficulty": "Medium",
        "question": "The students were divided ____ four groups.",
        "option_a": "in",
        "option_b": "into",
        "option_c": "on",
        "option_d": "at",
        "correct_answer": "B",
        "explanation": "The correct expression is 'divided into'."
    },

    {
        "topic": "Grammar",
        "subtopic": "Determiners",
        "difficulty": "Easy",
        "question": "There isn't ____ milk left in the refrigerator.",
        "option_a": "many",
        "option_b": "much",
        "option_c": "few",
        "option_d": "several",
        "correct_answer": "B",
        "explanation": "'Milk' is uncountable, so 'much' is used."
    },

    {
        "topic": "Grammar",
        "subtopic": "Determiners",
        "difficulty": "Easy",
        "question": "There are ____ students in the classroom.",
        "option_a": "much",
        "option_b": "little",
        "option_c": "many",
        "option_d": "less",
        "correct_answer": "C",
        "explanation": "'Students' is countable and plural, so 'many' is appropriate."
    },

    {
        "topic": "Oral English",
        "subtopic": "Rhyming Words",
        "difficulty": "Easy",
        "question": "Which word rhymes with 'day'?",
        "option_a": "die",
        "option_b": "say",
        "option_c": "do",
        "option_d": "dew",
        "correct_answer": "B",
        "explanation": "'Day' and 'say' have the same final vowel sound."
    },

    {
        "topic": "Oral English",
        "subtopic": "Vowel Sounds",
        "difficulty": "Medium",
        "question": "Which word has the same vowel sound as 'cup'?",
        "option_a": "food",
        "option_b": "luck",
        "option_c": "coop",
        "option_d": "cool",
        "correct_answer": "B",
        "explanation": "'Cup' and 'luck' contain the same short vowel sound."
    },

    {
        "topic": "Grammar",
        "subtopic": "Adverbs",
        "difficulty": "Medium",
        "question": "The athlete ran ____ to win the race.",
        "option_a": "quick",
        "option_b": "quickly",
        "option_c": "quickness",
        "option_d": "quickerly",
        "correct_answer": "B",
        "explanation": "The adverb 'quickly' modifies the verb 'ran'."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Meaning",
        "difficulty": "Hard",
        "question": "If a person is described as 'arrogant', the person is ____.",
        "option_a": "very humble",
        "option_b": "overly proud",
        "option_c": "very generous",
        "option_d": "extremely shy",
        "correct_answer": "B",
        "explanation": "Arrogant describes someone who has an exaggerated sense of superiority."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Meaning",
        "difficulty": "Medium",
        "question": "To 'mitigate' a problem means to ____ it.",
        "option_a": "make worse",
        "option_b": "reduce its severity",
        "option_c": "ignore completely",
        "option_d": "create",
        "correct_answer": "B",
        "explanation": "Mitigate means to make something less severe or harmful."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Word Meaning",
        "difficulty": "Hard",
        "question": "A 'novice' is a person who is ____.",
        "option_a": "highly experienced",
        "option_b": "new to an activity",
        "option_c": "very wealthy",
        "option_d": "extremely old",
        "correct_answer": "B",
        "explanation": "A novice is someone who is new or inexperienced."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "If a plan is 'up in the air', it is ____.",
        "option_a": "certain",
        "option_b": "undecided",
        "option_c": "completed",
        "option_d": "successful",
        "correct_answer": "B",
        "explanation": "An issue that is up in the air has not yet been decided."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "To 'get the ball rolling' means to ____.",
        "option_a": "start something",
        "option_b": "stop something",
        "option_c": "lose something",
        "option_d": "avoid something",
        "correct_answer": "A",
        "explanation": "The expression means to initiate an activity or process."
    },

    {
        "topic": "Grammar",
        "subtopic": "Sentence Structure",
        "difficulty": "Hard",
        "question": "Rarely ____ such an impressive performance.",
        "option_a": "we see",
        "option_b": "do we see",
        "option_c": "we saw",
        "option_d": "we have see",
        "correct_answer": "B",
        "explanation": "Negative or restrictive adverbs at the beginning require subject-verb inversion."
    },

    {
        "topic": "Grammar",
        "subtopic": "Sentence Structure",
        "difficulty": "Hard",
        "question": "Never ____ such a beautiful building before.",
        "option_a": "I have seen",
        "option_b": "have I seen",
        "option_c": "I saw",
        "option_d": "I see",
        "correct_answer": "B",
        "explanation": "Beginning with 'Never' requires inversion: 'have I seen'."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'ABUNDANT'.",
        "option_a": "plentiful",
        "option_b": "scarce",
        "option_c": "limited",
        "option_d": "rare",
        "correct_answer": "A",
        "explanation": "Abundant means available in large quantities."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the option opposite in meaning to 'ANONYMOUS'.",
        "option_a": "unknown",
        "option_b": "unidentified",
        "option_c": "identified",
        "option_d": "secret",
        "correct_answer": "C",
        "explanation": "Anonymous means unidentified or unnamed."
    },

    {
        "topic": "Grammar",
        "subtopic": "Relative Pronouns",
        "difficulty": "Medium",
        "question": "The woman ____ car was stolen reported the matter to the police.",
        "option_a": "who",
        "option_b": "whom",
        "option_c": "whose",
        "option_d": "which",
        "correct_answer": "C",
        "explanation": "'Whose' shows possession."
    },

    {
        "topic": "Grammar",
        "subtopic": "Pronouns",
        "difficulty": "Medium",
        "question": "This is the student ____ I told you about.",
        "option_a": "which",
        "option_b": "whom",
        "option_c": "whose",
        "option_d": "what",
        "correct_answer": "B",
        "explanation": "'Whom' can be used as the object of 'told you about' when referring to a person."
    },

    {
        "topic": "Sentence Completion",
        "subtopic": "Collocations",
        "difficulty": "Medium",
        "question": "The new law will ____ force next week.",
        "option_a": "come into",
        "option_b": "come at",
        "option_c": "come on",
        "option_d": "come by",
        "correct_answer": "A",
        "explanation": "The correct expression is 'come into force'."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Contextual Meaning",
        "difficulty": "Medium",
        "question": "The manager was impartial during the dispute. This means that he was ____.",
        "option_a": "biased",
        "option_b": "fair",
        "option_c": "angry",
        "option_d": "confused",
        "correct_answer": "B",
        "explanation": "Impartial means fair and not favouring either side."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Contextual Meaning",
        "difficulty": "Hard",
        "question": "The scientist's findings were remarkable. This means they were ____.",
        "option_a": "ordinary",
        "option_b": "noteworthy",
        "option_c": "irrelevant",
        "option_d": "unavailable",
        "correct_answer": "B",
        "explanation": "Remarkable means worthy of attention or unusually impressive."
    },

    {
        "topic": "Grammar",
        "subtopic": "Tenses",
        "difficulty": "Medium",
        "question": "I ____ my homework before my friend called.",
        "option_a": "finish",
        "option_b": "finished",
        "option_c": "had finished",
        "option_d": "have finish",
        "correct_answer": "C",
        "explanation": "The past perfect shows the homework was completed before another past event."
    },

    {
        "topic": "Grammar",
        "subtopic": "Tenses",
        "difficulty": "Easy",
        "question": "They ____ football when it started raining.",
        "option_a": "play",
        "option_b": "were playing",
        "option_c": "have played",
        "option_d": "will play",
        "correct_answer": "B",
        "explanation": "The past continuous describes an action in progress when another past event occurred."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Synonyms",
        "difficulty": "Medium",
        "question": "Choose the option nearest in meaning to 'CEASE'.",
        "option_a": "begin",
        "option_b": "continue",
        "option_c": "stop",
        "option_d": "increase",
        "correct_answer": "C",
        "explanation": "Cease means stop."
    },

    {
        "topic": "Vocabulary",
        "subtopic": "Antonyms",
        "difficulty": "Medium",
        "question": "Choose the option opposite in meaning to 'COURAGEOUS'.",
        "option_a": "brave",
        "option_b": "fearful",
        "option_c": "bold",
        "option_d": "confident",
        "correct_answer": "B",
        "explanation": "Fearful is opposite in meaning to courageous."
    },

    {
        "topic": "Idioms",
        "subtopic": "Meaning of Expressions",
        "difficulty": "Medium",
        "question": "If someone 'is on cloud nine', the person is ____.",
        "option_a": "very happy",
        "option_b": "very angry",
        "option_c": "very tired",
        "option_d": "very confused",
        "correct_answer": "A",
        "explanation": "The expression means to be extremely happy."
    },

    {
        "topic": "Grammar",
        "subtopic": "Concord",
        "difficulty": "Easy",
        "question": "My brother and sister ____ coming tomorrow.",
        "option_a": "is",
        "option_b": "was",
        "option_c": "are",
        "option_d": "has",
        "correct_answer": "C",
        "explanation": "Two subjects joined by 'and' normally take a plural verb."
    },

    {
        "topic": "Grammar",
        "subtopic": "Concord",
        "difficulty": "Medium",
        "question": "Mathematics ____ my favourite subject.",
        "option_a": "are",
        "option_b": "were",
        "option_c": "is",
        "option_d": "have",
        "correct_answer": "C",
        "explanation": "The name of the subject 'Mathematics' takes a singular verb."
    },

    {
        "topic": "Oral English",
        "subtopic": "Consonant Sounds",
        "difficulty": "Medium",
        "question": "Which word begins with the same sound as 'phone'?",
        "option_a": "fan",
        "option_b": "van",
        "option_c": "pan",
        "option_d": "ban",
        "correct_answer": "A",
        "explanation": "'Phone' and 'fan' begin with the /f/ sound."
    },

    {
        "topic": "Oral English",
        "subtopic": "Rhyming Words",
        "difficulty": "Easy",
        "question": "Which word rhymes with 'train'?",
        "option_a": "tree",
        "option_b": "brain",
        "option_c": "town",
        "option_d": "turn",
        "correct_answer": "B",
        "explanation": "'Train' and 'brain' have the same ending sound."
    },

]


# =========================================================
# INSERT QUESTIONS
# =========================================================

with app.app_context():

    added = 0
    skipped = 0

    for item in ENGLISH_QUESTIONS:

        existing = JAMBQuestion.query.filter_by(
            subject="Use of English",
            question=item["question"]
        ).first()

        if existing:
            skipped += 1
            continue

        new_question = JAMBQuestion(
            year=None,
            subject="Use of English",
            topic=item["topic"],
            subtopic=item["subtopic"],
            difficulty=item["difficulty"],
            question=item["question"],
            option_a=item["option_a"],
            option_b=item["option_b"],
            option_c=item["option_c"],
            option_d=item["option_d"],
            correct_answer=item["correct_answer"],
            explanation=item["explanation"],
            source="Career Bridge Original Practice Question"
        )

        db.session.add(new_question)

        added += 1

    db.session.commit()

    print("=" * 60)
    print("CAREER BRIDGE USE OF ENGLISH QUESTION BANK")
    print("=" * 60)
    print(f"Questions supplied: {len(ENGLISH_QUESTIONS)}")
    print(f"Questions added:    {added}")
    print(f"Questions skipped:  {skipped}")
    print("=" * 60)
