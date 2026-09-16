from src.weak_topic_detector import (
    detect_weak_topics
)


def test_dbms_topics():

    text = (
        "I am struggling with SQL joins "
        "and normalization in DBMS."
    )

    result = detect_weak_topics(
        text
    )

    topics = [
        item["topic"]
        for item in result
    ]

    assert "sql" in topics
    assert "joins" in topics
    assert "normalization" in topics


def test_machine_learning_topics():

    text = (
        "I find classification and "
        "overfitting difficult in machine learning."
    )

    result = detect_weak_topics(
        text
    )

    topics = [
        item["topic"]
        for item in result
    ]

    assert "classification" in topics
    assert "overfitting" in topics


def test_java_topics():

    text = (
        "I am struggling with "
        "polymorphism and collections in Java."
    )

    result = detect_weak_topics(
        text
    )

    topics = [
        item["topic"]
        for item in result
    ]

    assert "polymorphism" in topics
    assert "collections" in topics


def test_no_input():

    result = detect_weak_topics("")

    assert result == []