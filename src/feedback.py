# ============================================================
# STUDYWISE ADAPTIVE FEEDBACK ENGINE
# ============================================================


def calculate_completion(
    recommended_hours,
    actual_hours
):
    """
    Calculate percentage of recommended study time completed.
    """

    if recommended_hours <= 0:
        return 0

    completion = (
        actual_hours
        / recommended_hours
    ) * 100

    return min(completion, 100)


# ============================================================
# UPDATE PRIORITY
# ============================================================

def update_priority(
    current_priority,
    quiz_score,
    recommended_hours,
    actual_hours
):
    """
    Adapt priority based on quiz performance
    and study-time completion.

    The priority score is always kept between
    0 and 100.
    """

    # Make sure current score is valid

    current_priority = max(
        0,
        min(
            float(current_priority),
            100
        )
    )


    # --------------------------------------------------------
    # QUIZ ADJUSTMENT
    # --------------------------------------------------------

    if quiz_score < 40:

        quiz_adjustment = 10

    elif quiz_score < 60:

        quiz_adjustment = 6

    elif quiz_score < 75:

        quiz_adjustment = 2

    elif quiz_score < 90:

        quiz_adjustment = -3

    else:

        quiz_adjustment = -5


    # --------------------------------------------------------
    # STUDY COMPLETION
    # --------------------------------------------------------

    completion = calculate_completion(
        recommended_hours,
        actual_hours
    )


    if completion < 40:

        completion_adjustment = 5

    elif completion < 60:

        completion_adjustment = 3

    elif completion < 80:

        completion_adjustment = 0

    elif completion < 100:

        completion_adjustment = -2

    else:

        completion_adjustment = -3


    # --------------------------------------------------------
    # FINAL PRIORITY SCORE
    # --------------------------------------------------------

    priority_score = (

        current_priority
        + quiz_adjustment
        + completion_adjustment
    )


    # --------------------------------------------------------
    # KEEP SCORE BETWEEN 0 AND 100
    # --------------------------------------------------------

    priority_score = max(
        0,
        min(
            priority_score,
            100
        )
    )


    # --------------------------------------------------------
    # PRIORITY LEVEL
    # --------------------------------------------------------

    if priority_score >= 40:

        priority = "🔴 HIGH"

    elif priority_score >= 25:

        priority = "🟡 MEDIUM"

    else:

        priority = "🟢 LOW"


    return (
        priority_score,
        priority,
        completion
    )


# ============================================================
# GENERATE FEEDBACK
# ============================================================

def generate_feedback(
    quiz_score,
    recommended_hours,
    actual_hours
):
    """
    Generate personalized feedback messages.
    """

    messages = []


    # --------------------------------------------------------
    # QUIZ FEEDBACK
    # --------------------------------------------------------

    if quiz_score < 40:

        messages.append(
            "Your quiz score is low. "
            "Focus on the fundamentals and revise "
            "your weak topics."
        )

    elif quiz_score < 60:

        messages.append(
            "Your quiz performance needs improvement. "
            "Try solving more practice questions."
        )

    elif quiz_score < 75:

        messages.append(
            "Your quiz performance is moderate. "
            "Continue practicing to improve your understanding."
        )

    elif quiz_score < 90:

        messages.append(
            "Your quiz performance is good. "
            "Keep practicing to strengthen your knowledge."
        )

    else:

        messages.append(
            "Excellent quiz performance! "
            "Your understanding of this subject is strong."
        )


    # --------------------------------------------------------
    # STUDY COMPLETION
    # --------------------------------------------------------

    completion = calculate_completion(
        recommended_hours,
        actual_hours
    )


    if completion < 40:

        messages.append(
            "You completed less than 40% of your "
            "recommended study time. Try to increase "
            "your study consistency."
        )

    elif completion < 60:

        messages.append(
            "You completed less than 60% of your "
            "recommended study time."
        )

    elif completion < 80:

        messages.append(
            "You completed most of your recommended "
            "study time. Keep going."
        )

    elif completion < 100:

        messages.append(
            "You are very close to completing your "
            "recommended study time."
        )

    else:

        messages.append(
            "You completed your recommended study "
            "time successfully."
        )


    return messages


# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    current_priority = 50

    recommended_hours = 2

    actual_hours = 2

    quiz_score = 90


    new_score, priority, completion = (
        update_priority(
            current_priority,
            quiz_score,
            recommended_hours,
            actual_hours
        )
    )


    messages = generate_feedback(
        quiz_score,
        recommended_hours,
        actual_hours
    )


    print()
    print("🔄 StudyWise Adaptive Feedback")
    print("=" * 45)

    print(
        "Previous Priority:",
        current_priority
    )

    print(
        "Quiz Score:",
        quiz_score,
        "%"
    )

    print(
        "Recommended Study:",
        recommended_hours,
        "hours"
    )

    print(
        "Actual Study:",
        actual_hours,
        "hours"
    )

    print(
        "Completion:",
        round(
            completion,
            1
        ),
        "%"
    )

    print()

    print(
        "Updated Priority Score:",
        round(
            new_score,
            1
        )
    )

    print(
        "Updated Priority:",
        priority
    )

    print()

    print("💡 Feedback:")

    for message in messages:

        print(
            "•",
            message
        )