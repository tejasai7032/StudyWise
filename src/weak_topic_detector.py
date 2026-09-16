import re


# ===================================================
# SUBJECT TOPICS
# ===================================================

SUBJECT_TOPICS = {

    "Python": [
        "loops",
        "functions",
        "classes",
        "inheritance",
        "exception handling",
        "file handling"
    ],

    "Machine Learning": [
        "regression",
        "classification",
        "decision tree",
        "random forest",
        "clustering",
        "overfitting",
        "underfitting"
    ],

    "DBMS": [
        "sql",
        "joins",
        "normalization",
        "transactions",
        "keys",
        "indexes",
        "er diagram"
    ],

    "Operating Systems": [
        "process",
        "threads",
        "deadlock",
        "scheduling",
        "paging",
        "memory management"
    ],

    "Computer Networks": [
        "tcp",
        "udp",
        "ip",
        "routing",
        "osi",
        "dns",
        "http"
    ],

    "Java": [
        "inheritance",
        "polymorphism",
        "interfaces",
        "collections",
        "exceptions",
        "multithreading"
    ]
}


# ===================================================
# SUBJECT ALIASES
# ===================================================

SUBJECT_ALIASES = {

    "python": "Python",

    "machine learning": "Machine Learning",
    "machinelearning": "Machine Learning",
    "ml": "Machine Learning",

    "dbms": "DBMS",
    "database": "DBMS",
    "databases": "DBMS",

    "operating systems": "Operating Systems",
    "operating system": "Operating Systems",
    "os": "Operating Systems",

    "computer networks": "Computer Networks",
    "computer network": "Computer Networks",
    "networking": "Computer Networks",

    "java": "Java"
}


# ===================================================
# DETECT SUBJECTS
# ===================================================

def detect_subjects(text):

    text = text.lower()

    detected_subjects = []

    for alias, subject in SUBJECT_ALIASES.items():

        pattern = r"\b" + re.escape(alias) + r"\b"

        if re.search(pattern, text):

            if subject not in detected_subjects:

                detected_subjects.append(subject)

    return detected_subjects


# ===================================================
# DETECT TOPICS
# ===================================================

def detect_weak_topics(text):

    text = text.lower()

    detected_subjects = detect_subjects(text)

    detected_topics = []

    # -----------------------------------------------
    # If subject is mentioned, search only that
    # subject's topics
    # -----------------------------------------------

    if detected_subjects:

        subjects_to_search = detected_subjects

    else:

        # If no subject is mentioned, search topics
        # that are unique to one subject.

        subjects_to_search = list(
            SUBJECT_TOPICS.keys()
        )


    # -----------------------------------------------
    # Topic detection
    # -----------------------------------------------

    for subject in subjects_to_search:

        for topic in SUBJECT_TOPICS[subject]:

            pattern = r"\b" + re.escape(
                topic.lower()
            ) + r"\b"

            if re.search(pattern, text):

                detected_topics.append({
                    "subject": subject,
                    "topic": topic
                })


    # -----------------------------------------------
    # Remove duplicates
    # -----------------------------------------------

    unique_topics = []

    seen = set()

    for item in detected_topics:

        key = (
            item["subject"],
            item["topic"]
        )

        if key not in seen:

            seen.add(key)

            unique_topics.append(item)


    return unique_topics


# ===================================================
# TEST
# ===================================================

if __name__ == "__main__":

    examples = [

        (
            "I am struggling with SQL joins, "
            "normalization and transactions in DBMS."
        ),

        (
            "I find overfitting and classification "
            "difficult in machine learning."
        ),

        (
            "I am struggling with inheritance, "
            "polymorphism and collections in Java."
        ),

        (
            "I don't understand deadlock and "
            "process scheduling in operating systems."
        )
    ]


    for text in examples:

        print()
        print("Student:")
        print(text)

        print()
        print("Detected:")

        topics = detect_weak_topics(text)

        for topic in topics:

            print(
                f"  {topic['subject']} → "
                f"{topic['topic']}"
            )

        print("-" * 50)