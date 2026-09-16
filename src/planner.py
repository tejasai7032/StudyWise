def calculate_daily_hours(total_hours, days_remaining):
    """
    Calculate the average study hours needed per day.
    """

    if days_remaining <= 0:
        return 0

    return total_hours / days_remaining


def allocate_study_time(subjects, available_hours):
    """
    Allocate available daily study time between subjects
    based on their predicted study requirements.
    """

    total_required_hours = sum(
        subject["study_hours"]
        for subject in subjects
    )

    if total_required_hours <= 0:
        return subjects

    for subject in subjects:

        proportion = (
            subject["study_hours"]
            / total_required_hours
        )

        subject["daily_hours"] = (
            proportion * available_hours
        )

    return subjects


if __name__ == "__main__":

    subjects = [
        {
            "name": "Machine Learning",
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

    available_hours = 3

    plan = allocate_study_time(
        subjects,
        available_hours
    )

    print("📚 Daily Study Plan")
    print()

    for subject in plan:

        print(
            subject["name"],
            "→",
            round(subject["daily_hours"], 2),
            "hours/day"
        )