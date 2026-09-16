# ============================================================
# STUDYWISE — FLASK BACKEND
# AI-POWERED PERSONALIZED STUDY PLANNER
# ============================================================

from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

from src.weak_topic_detector import detect_weak_topics

from src.feedback import (
    update_priority,
    generate_feedback
)


# ------------------------------------------------------------
# APP CONFIGURATION
# ------------------------------------------------------------

app = Flask(__name__)

MODEL_PATH = "models/study_hours_model.pkl"

model = joblib.load(MODEL_PATH)


# ------------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------------

@app.route("/")
def home():
    return render_template("index.html")


# ------------------------------------------------------------
# GENERATE STUDY PLAN
# ------------------------------------------------------------

@app.route("/generate-plan", methods=["POST"])
def generate_plan():

    try:

        data = request.get_json()

        if not data:
            return jsonify({
                "success": False,
                "error": "No input data received."
            }), 400


        # ----------------------------------------------------
        # GET SUBJECTS
        # ----------------------------------------------------

        subjects = data.get("subjects", [])


        # Backward compatibility with old single-subject UI
        if not subjects:

            old_subject = data.get(
                "subject",
                "Machine Learning"
            )

            subjects = [
                {
                    "name": old_subject,
                    "previousMarks": data.get(
                        "previousMarks",
                        60
                    ),
                    "currentMarks": data.get(
                        "currentMarks",
                        62
                    ),
                    "difficulty": data.get(
                        "difficulty",
                        3
                    ),
                    "daysRemaining": data.get(
                        "daysRemaining",
                        25
                    ),
                    "confidence": data.get(
                        "confidence",
                        3
                    ),
                    "previousStudy": data.get(
                        "previousStudy",
                        15
                    )
                }
            ]


        # ----------------------------------------------------
        # AVAILABLE DAILY HOURS
        # ----------------------------------------------------

        available_hours = float(
            data.get(
                "availableHours",
                3
            )
        )

        available_hours = max(
            0.5,
            min(
                available_hours,
                10
            )
        )


        # ----------------------------------------------------
        # WEAK TOPIC TEXT
        # ----------------------------------------------------

        weak_topic_text = data.get(
            "weakTopics",
            ""
        )

        detected_topics = []


        if weak_topic_text.strip():

            detected_topics = detect_weak_topics(
                weak_topic_text
            )


        # ----------------------------------------------------
        # PROCESS EACH SUBJECT
        # ----------------------------------------------------

        results = []


        for subject_data in subjects:

            subject = subject_data.get(
                "name",
                "Unknown Subject"
            )


            previous_marks = float(
                subject_data.get(
                    "previousMarks",
                    60
                )
            )

            current_marks = float(
                subject_data.get(
                    "currentMarks",
                    62
                )
            )

            difficulty = float(
                subject_data.get(
                    "difficulty",
                    3
                )
            )

            days_remaining = float(
                subject_data.get(
                    "daysRemaining",
                    25
                )
            )

            confidence = float(
                subject_data.get(
                    "confidence",
                    3
                )
            )

            previous_study_hours = float(
                subject_data.get(
                    "previousStudy",
                    15
                )
            )


            # ------------------------------------------------
            # INPUT VALIDATION
            # ------------------------------------------------

            previous_marks = max(
                0,
                min(
                    previous_marks,
                    100
                )
            )

            current_marks = max(
                0,
                min(
                    current_marks,
                    100
                )
            )

            difficulty = max(
                1,
                min(
                    difficulty,
                    5
                )
            )

            days_remaining = max(
                days_remaining,
                1
            )

            confidence = max(
                1,
                min(
                    confidence,
                    5
                )
            )

            previous_study_hours = max(
                previous_study_hours,
                0
            )


            # ------------------------------------------------
            # ML INPUT
            # ------------------------------------------------

            student = pd.DataFrame({

                "previous_marks": [
                    previous_marks
                ],

                "current_marks": [
                    current_marks
                ],

                "difficulty": [
                    difficulty
                ],

                "days_remaining": [
                    days_remaining
                ],

                "confidence": [
                    confidence
                ],

                "previous_study_hours": [
                    previous_study_hours
                ],

                "available_hours": [
                    available_hours
                ]

            })


            # ------------------------------------------------
            # RANDOM FOREST PREDICTION
            # ------------------------------------------------

            prediction = model.predict(
                student
            )[0]


            prediction = max(
                0.5,
                min(
                    float(prediction),
                    10
                )
            )


            # ------------------------------------------------
            # RULE-BASED PRIORITY SCORE
            # ------------------------------------------------

            priority_score = (

                (100 - current_marks) * 0.4

                + difficulty * 8

                + (6 - confidence) * 8

            )


            # ------------------------------------------------
            # NLP WEAK TOPIC BOOST
            # ------------------------------------------------

            subject_has_weak_topic = any(

                topic["subject"] == subject

                for topic in detected_topics

            )


            if subject_has_weak_topic:

                priority_score += 10


            priority_score = max(
                0,
                min(
                    priority_score,
                    100
                )
            )


            # ------------------------------------------------
            # PRIORITY LABEL
            # ------------------------------------------------

            if priority_score >= 40:

                priority = "🔴 HIGH"

            elif priority_score >= 25:

                priority = "🟡 MEDIUM"

            else:

                priority = "🟢 LOW"


            # ------------------------------------------------
            # SAVE RESULT
            # ------------------------------------------------

            results.append({

                "subject": subject,

                "study_hours": round(
                    prediction,
                    2
                ),

                "priority_score": round(
                    priority_score,
                    1
                ),

                "priority": priority,

                "days_remaining": int(
                    days_remaining
                ),

                "weak_topic":
                    subject_has_weak_topic

            })


        # ----------------------------------------------------
        # ALLOCATE DAILY STUDY TIME
        # ----------------------------------------------------

        total_required_hours = sum(

            result["study_hours"]

            for result in results

        )


        if total_required_hours > 0:

            for result in results:

                proportion = (

                    result["study_hours"]

                    / total_required_hours

                )

                result["daily_hours"] = round(

                    proportion
                    * available_hours,

                    2

                )

        else:

            for result in results:

                result["daily_hours"] = 0


        # ----------------------------------------------------
        # TOTAL DAILY HOURS
        # ----------------------------------------------------

        total_daily_hours = sum(

            result["daily_hours"]

            for result in results

        )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "subjects": results,

            "detected_topics":
                detected_topics,

            "total_required_hours":
                round(
                    total_required_hours,
                    2
                ),

            "total_daily_hours":
                round(
                    total_daily_hours,
                    2
                ),

            "available_hours":
                available_hours

        })


    except Exception as error:

        print(
            "Generate Plan Error:",
            error
        )

        return jsonify({

            "success": False,

            "error": str(error)

        }), 400


# ------------------------------------------------------------
# ADAPTIVE FEEDBACK
# ------------------------------------------------------------

@app.route(
    "/update-feedback",
    methods=["POST"]
)
def update_feedback():

    try:

        data = request.get_json()


        if not data:

            return jsonify({

                "success": False,

                "error":
                    "No feedback data received."

            }), 400


        current_priority = float(

            data.get(
                "currentPriority",
                50
            )

        )


        quiz_score = float(

            data.get(
                "quizScore",
                60
            )

        )


        recommended_hours = float(

            data.get(
                "recommendedHours",
                2
            )

        )


        actual_hours = float(

            data.get(
                "actualHours",
                1
            )

        )


        # ----------------------------------------------------
        # VALIDATION
        # ----------------------------------------------------

        current_priority = max(

            0,

            min(
                current_priority,
                100
            )

        )


        quiz_score = max(

            0,

            min(
                quiz_score,
                100
            )

        )


        recommended_hours = max(

            0,

            recommended_hours

        )


        actual_hours = max(

            0,

            min(
                actual_hours,
                10
            )

        )


        # ----------------------------------------------------
        # UPDATE PRIORITY
        # ----------------------------------------------------

        (
            new_score,
            new_priority,
            completion

        ) = update_priority(

            current_priority,

            quiz_score,

            recommended_hours,

            actual_hours

        )


        # ----------------------------------------------------
        # GENERATE FEEDBACK
        # ----------------------------------------------------

        messages = generate_feedback(

            quiz_score,

            recommended_hours,

            actual_hours

        )


        # ----------------------------------------------------
        # RESPONSE
        # ----------------------------------------------------

        return jsonify({

            "success": True,

            "old_score":
                round(
                    current_priority,
                    1
                ),

            "new_score":
                round(
                    new_score,
                    1
                ),

            "priority":
                new_priority,

            "completion":
                round(
                    completion,
                    1
                ),

            "messages":
                messages

        })


    except Exception as error:

        print(
            "Feedback Error:",
            error
        )

        return jsonify({

            "success": False,

            "error": str(error)

        }), 400


# ------------------------------------------------------------
# HEALTH CHECK
# ------------------------------------------------------------

@app.route(
    "/health",
    methods=["GET"]
)
def health_check():

    return jsonify({

        "status": "healthy",

        "application": "StudyWise",

        "model":
            "Random Forest Regressor",

        "services": [

            "Multi-Subject ML Prediction",

            "NLP Weak Topic Detection",

            "Priority Engine",

            "Study Time Allocation",

            "Adaptive Feedback"

        ]

    })


# ------------------------------------------------------------
# RUN APPLICATION
# ------------------------------------------------------------

if __name__ == "__main__":

    print()

    print(
        "=" * 60
    )

    print(
        "📚 STUDYWISE"
    )

    print(
        "AI-Powered Personalized Study Planner"
    )

    print(
        "=" * 60
    )

    print()

    print(
        "🚀 Flask server starting..."
    )

    print()

    print(
        "🌐 Website:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print()

    print(
        "❤️ Health:"
    )

    print(
        "http://127.0.0.1:5000/health"
    )

    print()

    print(
        "Press CTRL+C to stop."
    )

    print()


    app.run(

        host="127.0.0.1",

        port=5000,

        debug=True

    )