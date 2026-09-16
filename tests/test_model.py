import joblib
import pandas as pd


def test_model_exists():

    model = joblib.load(
        "models/study_hours_model.pkl"
    )

    assert model is not None


def test_model_prediction():

    model = joblib.load(
        "models/study_hours_model.pkl"
    )

    student = pd.DataFrame({

        "previous_marks": [60],

        "current_marks": [62],

        "difficulty": [4],

        "days_remaining": [20],

        "confidence": [3],

        "previous_study_hours": [15],

        "available_hours": [5]
    })


    prediction = model.predict(
        student
    )


    assert len(prediction) == 1


def test_prediction_is_number():

    model = joblib.load(
        "models/study_hours_model.pkl"
    )


    student = pd.DataFrame({

        "previous_marks": [70],

        "current_marks": [65],

        "difficulty": [3],

        "days_remaining": [15],

        "confidence": [3],

        "previous_study_hours": [20],

        "available_hours": [5]
    })


    prediction = model.predict(
        student
    )[0]


    assert isinstance(
        prediction,
        float
    )


def test_prediction_is_positive():

    model = joblib.load(
        "models/study_hours_model.pkl"
    )


    student = pd.DataFrame({

        "previous_marks": [50],

        "current_marks": [45],

        "difficulty": [5],

        "days_remaining": [5],

        "confidence": [1],

        "previous_study_hours": [10],

        "available_hours": [5]
    })


    prediction = model.predict(
        student
    )[0]


    assert prediction > 0