from src.planner import (
    calculate_daily_hours,
    allocate_study_time
)


def test_daily_hours_calculation():

    result = calculate_daily_hours(
        20,
        10
    )

    assert result == 2


def test_zero_days():

    result = calculate_daily_hours(
        20,
        0
    )

    assert result == 0


def test_negative_days():

    result = calculate_daily_hours(
        20,
        -5
    )

    assert result == 0


def test_allocate_study_time():

    subjects = [

        {
            "name": "ML",
            "study_hours": 30
        },

        {
            "name": "DBMS",
            "study_hours": 20
        },

        {
            "name": "Python",
            "study_hours": 10
        }
    ]

    result = allocate_study_time(
        subjects,
        3
    )

    total_daily_hours = sum(
        subject["daily_hours"]
        for subject in result
    )

    assert round(
        total_daily_hours,
        2
    ) == 3


def test_all_subjects_receive_time():

    subjects = [

        {
            "name": "ML",
            "study_hours": 30
        },

        {
            "name": "DBMS",
            "study_hours": 20
        }
    ]

    result = allocate_study_time(
        subjects,
        4
    )

    for subject in result:

        assert subject["daily_hours"] > 0