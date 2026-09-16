import joblib
import pandas as pd


# Load the trained model
model = joblib.load("models/study_hours_model.pkl")


# Information about a new student
student = pd.DataFrame({
    "previous_marks": [60],
    "current_marks": [62],
    "difficulty": [5],
    "days_remaining": [25],
    "confidence": [2],
    "previous_study_hours": [15],
    "available_hours": [3]
})


# Make prediction
prediction = model.predict(student)


print("Predicted study hours:", round(prediction[0], 2))