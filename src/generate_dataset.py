import pandas as pd
import random


# Make results reproducible
random.seed(42)


rows = []


# ---------------------------------------------------
# GENERATE SYNTHETIC STUDENT DATA
# ---------------------------------------------------

for i in range(500):

    previous_marks = random.randint(40, 95)

    current_marks = random.randint(40, 95)

    difficulty = random.randint(1, 5)

    days_remaining = random.randint(3, 60)

    confidence = random.randint(1, 5)

    previous_study_hours = round(
        random.uniform(5, 50),
        1
    )

    available_hours = round(
        random.uniform(1, 6),
        1
    )


    # ------------------------------------------------
    # SIMULATED STUDY-HOUR REQUIREMENT
    # ------------------------------------------------
    #
    # This formula creates the target variable.
    # It is synthetic data, NOT real student data.
    #

    recommended_hours = (

        (100 - current_marks) * 0.20

        + difficulty * 2.5

        + (6 - confidence) * 2

        + max(0, 20 - days_remaining) * 0.25

        + max(0, previous_marks - current_marks) * 0.10

        - previous_study_hours * 0.03

    )


    # Add small random variation
    recommended_hours += random.uniform(-2, 2)


    # Keep value within a reasonable range
    recommended_hours = max(
        5,
        min(recommended_hours, 50)
    )


    rows.append({

        "previous_marks": previous_marks,

        "current_marks": current_marks,

        "difficulty": difficulty,

        "days_remaining": days_remaining,

        "confidence": confidence,

        "previous_study_hours": previous_study_hours,

        "available_hours": available_hours,

        "recommended_study_hours": round(
            recommended_hours,
            2
        )

    })


# ---------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------

data = pd.DataFrame(rows)


# ---------------------------------------------------
# SAVE DATASET
# ---------------------------------------------------

data.to_csv(
    "data/study_data.csv",
    index=False
)


print("✅ Dataset generated successfully!")

print()

print("Number of records:")
print(len(data))

print()

print("Dataset shape:")
print(data.shape)

print()

print("First 5 rows:")
print(data.head())