from src.feedback import (
    calculate_completion,
    update_priority,
    generate_feedback
)


def test_completion_full():

    completion = calculate_completion(
        2,
        2
    )

    assert completion == 100


def test_completion_half():

    completion = calculate_completion(
        4,
        2
    )

    assert completion == 50


def test_completion_never_above_100():

    completion = calculate_completion(
        2,
        5
    )

    assert completion == 100


def test_high_quiz_reduces_priority():

    old_score = 50

    new_score, priority, completion = (
        update_priority(
            old_score,
            95,
            2,
            2
        )
    )

    assert new_score < old_score


def test_low_quiz_increases_priority():

    old_score = 30

    new_score, priority, completion = (
        update_priority(
            old_score,
            30,
            2,
            1
        )
    )

    assert new_score > old_score


def test_priority_never_negative():

    new_score, priority, completion = (
        update_priority(
            0,
            100,
            2,
            2
        )
    )

    assert new_score >= 0


def test_priority_never_above_100():

    new_score, priority, completion = (
        update_priority(
            100,
            20,
            2,
            0
        )
    )

    assert new_score <= 100


def test_high_priority_label():

    score, priority, completion = (
        update_priority(
            50,
            30,
            2,
            0
        )
    )

    assert priority == "🔴 HIGH"


def test_feedback_returns_messages():

    messages = generate_feedback(
        90,
        2,
        2
    )

    assert len(messages) > 0