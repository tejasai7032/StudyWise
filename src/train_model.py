import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ===================================================
# LOAD DATASET
# ===================================================

data = pd.read_csv("data/study_data.csv")

print("Dataset loaded successfully!")
print("Dataset shape:", data.shape)


# ===================================================
# FEATURES AND TARGET
# ===================================================

X = data[
    [
        "previous_marks",
        "current_marks",
        "difficulty",
        "days_remaining",
        "confidence",
        "previous_study_hours",
        "available_hours"
    ]
]

y = data["recommended_study_hours"]


# ===================================================
# TRAIN / TEST SPLIT
# ===================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


print()
print("Training samples:", len(X_train))
print("Testing samples:", len(X_test))


# ===================================================
# CREATE MODEL
# ===================================================

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)


# ===================================================
# TRAIN MODEL
# ===================================================

model.fit(X_train, y_train)

print()
print("✅ Model training completed!")


# ===================================================
# PREDICTIONS
# ===================================================

predictions = model.predict(X_test)


# ===================================================
# MODEL EVALUATION
# ===================================================

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

r2 = r2_score(
    y_test,
    predictions
)


print()
print("📊 Model Evaluation")
print("=" * 40)

print(
    f"Mean Absolute Error (MAE): {mae:.2f}"
)

print(
    f"Root Mean Squared Error (RMSE): {rmse:.2f}"
)

print(
    f"R² Score: {r2:.2f}"
)


# ===================================================
# FEATURE IMPORTANCE
# ===================================================

feature_importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance": model.feature_importances_

}).sort_values(
    by="Importance",
    ascending=False
)


print()
print("🔍 Feature Importance")
print("=" * 40)

print(feature_importance)


# ===================================================
# SAVE MODEL
# ===================================================

joblib.dump(
    model,
    "models/study_hours_model.pkl"
)

print()
print("✅ New model saved successfully!")

print(
    "Location: models/study_hours_model.pkl"
)