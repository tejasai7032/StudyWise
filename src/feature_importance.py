import joblib
import pandas as pd


# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

model = joblib.load(
    "models/study_hours_model.pkl"
)


# ---------------------------------------------------
# FEATURE NAMES
# ---------------------------------------------------

features = [
    "Previous Marks",
    "Current Marks",
    "Difficulty",
    "Days Remaining",
    "Confidence",
    "Previous Study Hours",
    "Available Hours"
]


# ---------------------------------------------------
# GET FEATURE IMPORTANCE
# ---------------------------------------------------

importance = model.feature_importances_


# ---------------------------------------------------
# CREATE DATAFRAME
# ---------------------------------------------------

importance_data = pd.DataFrame({
    "Feature": features,
    "Importance": importance
})


# Sort from highest to lowest
importance_data = importance_data.sort_values(
    by="Importance",
    ascending=False
)


# ---------------------------------------------------
# DISPLAY
# ---------------------------------------------------

print("🔍 Feature Importance")
print("=" * 40)

for _, row in importance_data.iterrows():

    print(
        f"{row['Feature']:<25} "
        f"{row['Importance']:.3f}"
    )