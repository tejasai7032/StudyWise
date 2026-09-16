import streamlit as st
import joblib
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

from src.weak_topic_detector import detect_weak_topics

from src.feedback import (
    update_priority,
    generate_feedback
)

from src.feature_importance import importance_data


# ============================================================
# LOAD MODEL
# ============================================================

model = joblib.load(
    "models/study_hours_model.pkl"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="StudyWise",
    page_icon="📚",
    layout="centered"
)


# ============================================================
# SESSION STATE
# ============================================================

if "results" not in st.session_state:
    st.session_state.results = None

if "detected_topics" not in st.session_state:
    st.session_state.detected_topics = []

if "plan_generated" not in st.session_state:
    st.session_state.plan_generated = False

if "feedback_result" not in st.session_state:
    st.session_state.feedback_result = None


# ============================================================
# TITLE
# ============================================================

st.title("📚 StudyWise")

st.subheader(
    "AI-Powered Personalized Study Planner"
)

st.write(
    "StudyWise uses Machine Learning and NLP to "
    "analyze academic performance, detect weak "
    "topics and create a personalized study plan."
)

st.info(
    "⏱️ StudyWise plans a maximum of "
    "**10 study hours per day** and automatically "
    "adds structured study breaks."
)


# ============================================================
# SUBJECT SELECTION
# ============================================================

st.header("📚 Select Subjects")

subjects = st.multiselect(
    "Choose the subjects you want to study:",
    [
        "Python",
        "Machine Learning",
        "DBMS",
        "Operating Systems",
        "Computer Networks",
        "Mathematics",
        "Java"
    ]
)


# ============================================================
# DAILY STUDY HOURS
# ============================================================

st.header("⏰ Daily Study Availability")

available_daily_hours = st.number_input(
    "Maximum Study Hours Per Day",
    min_value=0.5,
    max_value=10.0,
    value=3.0,
    step=0.5
)

st.caption(
    "Maximum allowed study time is 10 hours per day."
)


# ============================================================
# START TIME
# ============================================================

start_time = st.time_input(
    "🕘 Preferred Study Start Time",
    value=datetime.strptime(
        "09:00",
        "%H:%M"
    ).time()
)


# ============================================================
# WEAK TOPIC DETECTION
# ============================================================

st.header("🧠 Weak Topic Detection")

weak_topic_text = st.text_area(
    "Tell StudyWise what topics you are struggling with:",
    placeholder=(
        "Example: I am struggling with SQL joins, "
        "normalization and transactions in DBMS."
    ),
    height=120
)


# ============================================================
# SUBJECT INFORMATION
# ============================================================

subject_data = {}


if subjects:

    st.header("📝 Subject Information")

    for subject in subjects:

        st.subheader(
            f"📖 {subject}"
        )

        previous_marks = st.number_input(
            f"{subject} - Previous Marks",
            min_value=0,
            max_value=100,
            value=60,
            key=f"{subject}_previous"
        )

        current_marks = st.number_input(
            f"{subject} - Current Marks",
            min_value=0,
            max_value=100,
            value=62,
            key=f"{subject}_current"
        )

        difficulty = st.slider(
            f"{subject} - Difficulty",
            min_value=1,
            max_value=5,
            value=3,
            key=f"{subject}_difficulty"
        )

        days_remaining = st.number_input(
            f"{subject} - Days Remaining",
            min_value=1,
            max_value=365,
            value=25,
            key=f"{subject}_days"
        )

        confidence = st.slider(
            f"{subject} - Confidence Level",
            min_value=1,
            max_value=5,
            value=3,
            key=f"{subject}_confidence"
        )

        previous_study_hours = st.number_input(
            f"{subject} - Previous Study Hours",
            min_value=0.0,
            max_value=500.0,
            value=15.0,
            key=f"{subject}_study"
        )

        subject_data[subject] = {

            "previous_marks":
                previous_marks,

            "current_marks":
                current_marks,

            "difficulty":
                difficulty,

            "days_remaining":
                days_remaining,

            "confidence":
                confidence,

            "previous_study_hours":
                previous_study_hours
        }


# ============================================================
# GENERATE PLAN
# ============================================================

if st.button(
    "🎯 Generate Personalized Plan"
):

    if not subjects:

        st.warning(
            "Please select at least one subject."
        )

    else:

        # ----------------------------------------------------
        # DETECT WEAK TOPICS
        # ----------------------------------------------------

        detected_topics = []

        if weak_topic_text.strip():

            detected_topics = detect_weak_topics(
                weak_topic_text
            )

        st.session_state.detected_topics = (
            detected_topics
        )


        # ----------------------------------------------------
        # RESULTS
        # ----------------------------------------------------

        results = []


        for subject in subjects:

            info = subject_data[subject]


            # ------------------------------------------------
            # MODEL INPUT
            # ------------------------------------------------

            student = pd.DataFrame({

                "previous_marks": [
                    info["previous_marks"]
                ],

                "current_marks": [
                    info["current_marks"]
                ],

                "difficulty": [
                    info["difficulty"]
                ],

                "days_remaining": [
                    info["days_remaining"]
                ],

                "confidence": [
                    info["confidence"]
                ],

                "previous_study_hours": [
                    info["previous_study_hours"]
                ],

                "available_hours": [
                    available_daily_hours
                ]
            })


            # ------------------------------------------------
            # ML PREDICTION
            # ------------------------------------------------

            prediction = model.predict(
                student
            )[0]


            # ------------------------------------------------
            # LIMIT TO 10 HOURS
            # ------------------------------------------------

            prediction = max(
                0.5,
                min(
                    float(prediction),
                    10.0
                )
            )


            # ------------------------------------------------
            # PRIORITY SCORE
            # ------------------------------------------------

            priority_score = (

                (100 - info["current_marks"])
                * 0.4

                + info["difficulty"]
                * 8

                + (6 - info["confidence"])
                * 8
            )


            # ------------------------------------------------
            # WEAK TOPIC BOOST
            # ------------------------------------------------

            subject_has_weak_topic = any(

                topic["subject"] == subject

                for topic in detected_topics
            )


            if subject_has_weak_topic:

                priority_score += 10


            # ------------------------------------------------
            # PRIORITY LEVEL
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

                "Subject":
                    subject,

                "Study Hours":
                    prediction,

                "Days Remaining":
                    int(
                        info["days_remaining"]
                    ),

                "Priority Score":
                    float(
                        priority_score
                    ),

                "Priority":
                    priority
            })


        # ====================================================
        # TOTAL REQUIRED HOURS
        # ====================================================

        total_required_hours = sum(

            result["Study Hours"]

            for result in results
        )


        # ====================================================
        # DAILY HOURS ALLOCATION
        # ====================================================

        if total_required_hours > 0:

            for result in results:

                proportion = (

                    result["Study Hours"]
                    /
                    total_required_hours
                )


                daily_hours = (

                    proportion
                    *
                    available_daily_hours
                )


                # Never exceed 10 hours
                daily_hours = min(
                    daily_hours,
                    10.0
                )


                result["Daily Hours"] = (
                    daily_hours
                )


        # ====================================================
        # SAVE
        # ====================================================

        st.session_state.results = results

        st.session_state.plan_generated = True

        st.session_state.feedback_result = None


# ============================================================
# FUNCTION:
# CREATE STUDY SCHEDULE
# ============================================================

def create_study_schedule(
    study_hours,
    start_time
):

    """
    Creates detailed study and break schedule.

    Study session:
        50 minutes

    Normal break:
        10 minutes

    Long break:
        20 minutes after every 3 sessions
    """

    schedule = []

    total_study_minutes = int(
        round(
            study_hours * 60
        )
    )


    remaining_minutes = (
        total_study_minutes
    )


    current_time = datetime.combine(
        datetime.today(),
        start_time
    )


    session_number = 0


    while remaining_minutes > 0:

        # ----------------------------------------------------
        # STUDY SESSION
        # ----------------------------------------------------

        session_number += 1


        session_minutes = min(
            50,
            remaining_minutes
        )


        study_start = current_time

        study_end = (
            study_start
            + timedelta(
                minutes=session_minutes
            )
        )


        schedule.append({

            "Type":
                "📚 Study",

            "Session":
                f"Study Session {session_number}",

            "Start":
                study_start.strftime(
                    "%I:%M %p"
                ),

            "End":
                study_end.strftime(
                    "%I:%M %p"
                ),

            "Duration":
                f"{session_minutes} min"
        })


        current_time = study_end

        remaining_minutes -= (
            session_minutes
        )


        # ----------------------------------------------------
        # BREAK
        # ----------------------------------------------------

        if remaining_minutes > 0:

            if session_number % 3 == 0:

                break_minutes = 20

                break_type = (
                    "🧘 Long Break"
                )

            else:

                break_minutes = 10

                break_type = (
                    "☕ Short Break"
                )


            break_start = current_time

            break_end = (
                break_start
                + timedelta(
                    minutes=break_minutes
                )
            )


            schedule.append({

                "Type":
                    break_type,

                "Session":
                    "Break",

                "Start":
                    break_start.strftime(
                        "%I:%M %p"
                    ),

                "End":
                    break_end.strftime(
                        "%I:%M %p"
                    ),

                "Duration":
                    f"{break_minutes} min"
            })


            current_time = break_end


    return schedule


# ============================================================
# DISPLAY PLAN
# ============================================================

if st.session_state.plan_generated:

    results = st.session_state.results

    detected_topics = (
        st.session_state.detected_topics
    )


    # ========================================================
    # WEAK TOPICS
    # ========================================================

    st.header(
        "🔍 Detected Weak Topics"
    )


    if detected_topics:

        for topic in detected_topics:

            st.write(

                f"📚 **{topic['subject']}** → "
                f"{topic['topic']}"
            )

    else:

        st.info(
            "No specific weak topics detected."
        )


    # ========================================================
    # PERSONALIZED PLAN
    # ========================================================

    st.header(
        "🎯 Your Personalized Study Plan"
    )


    for result in results:

        st.subheader(
            f"📖 {result['Subject']}"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(

                "Total Study",

                f"{result['Study Hours']:.1f} hrs"
            )


        with col2:

            st.metric(

                "Daily Study",

                f"{result['Daily Hours']:.1f} hrs"
            )


        with col3:

            st.metric(

                "Days Left",

                result["Days Remaining"]
            )


        st.write(

            f"Priority Score: "
            f"**{result['Priority Score']:.1f}**"
        )


        st.write(

            f"Priority: "
            f"**{result['Priority']}**"
        )


        st.divider()


    # ========================================================
    # DAILY SCHEDULE
    # ========================================================

    st.header(
        "🗓️ Detailed Daily Timetable"
    )


    st.write(

        "StudyWise divides your study time into "
        "**50-minute focused sessions** followed by "
        "**10-minute breaks**. After every three "
        "sessions, a **20-minute long break** is provided."
    )


    # --------------------------------------------------------
    # TOTALS
    # --------------------------------------------------------

    total_daily_study_minutes = int(
        round(
            sum(
                result["Daily Hours"]
                for result in results
            )
            * 60
        )
    )


    total_break_minutes = 0

    all_schedule_rows = []


    # --------------------------------------------------------
    # CREATE SCHEDULE FOR EACH SUBJECT
    # --------------------------------------------------------

    current_schedule_start = start_time


    for result in results:

        subject_hours = (
            result["Daily Hours"]
        )


        subject_schedule = (
            create_study_schedule(
                subject_hours,
                current_schedule_start
            )
        )


        # ----------------------------------------------------
        # ADD SUBJECT NAME
        # ----------------------------------------------------

        for row in subject_schedule:

            row["Subject"] = (
                result["Subject"]
            )

            all_schedule_rows.append(
                row
            )


            if "Break" in row["Type"]:

                duration = int(
                    row["Duration"].split()[0]
                )

                total_break_minutes += (
                    duration
                )


        # ----------------------------------------------------
        # FIND END TIME
        # ----------------------------------------------------

        if subject_schedule:

            last_row = (
                subject_schedule[-1]
            )


            current_schedule_start = (
                datetime.strptime(
                    last_row["End"],
                    "%I:%M %p"
                ).time()
            )


    # --------------------------------------------------------
    # DISPLAY TIMETABLE
    # --------------------------------------------------------

    if all_schedule_rows:

        schedule_df = pd.DataFrame(
            all_schedule_rows
        )


        schedule_df = schedule_df[
            [
                "Subject",
                "Type",
                "Session",
                "Start",
                "End",
                "Duration"
            ]
        ]


        st.dataframe(

            schedule_df,

            use_container_width=True,

            hide_index=True
        )


    # ========================================================
    # TIME SUMMARY
    # ========================================================

    total_schedule_minutes = (

        total_daily_study_minutes
        +
        total_break_minutes
    )


    study_hours_display = (
        total_daily_study_minutes
        // 60
    )

    study_minutes_display = (
        total_daily_study_minutes
        % 60
    )


    schedule_hours_display = (
        total_schedule_minutes
        // 60
    )

    schedule_minutes_display = (
        total_schedule_minutes
        % 60
    )


    st.subheader(
        "⏱️ Daily Time Summary"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(

            "📚 Study Time",

            f"{study_hours_display}h "
            f"{study_minutes_display}m"
        )


    with col2:

        st.metric(

            "☕ Break Time",

            f"{total_break_minutes // 60}h "
            f"{total_break_minutes % 60}m"
        )


    with col3:

        st.metric(

            "🕐 Total Schedule",

            f"{schedule_hours_display}h "
            f"{schedule_minutes_display}m"
        )


    # ========================================================
    # BREAK INFORMATION
    # ========================================================

    st.subheader(
        "☕ Break Details"
    )


    st.write(
        "• **Short Break:** 10 minutes after "
        "each 50-minute study session."
    )

    st.write(
        "• **Long Break:** 20 minutes after "
        "every 3 study sessions."
    )

    st.write(
        f"• **Total Break Time Today:** "
        f"{total_break_minutes} minutes."
    )


    # ========================================================
    # STUDY PLAN TABLE
    # ========================================================

    st.header(
        "📊 Study Plan Summary"
    )


    table_data = []


    for result in results:

        table_data.append({

            "Subject":
                result["Subject"],

            "Total Hours":
                round(
                    result["Study Hours"],
                    2
                ),

            "Daily Hours":
                round(
                    result["Daily Hours"],
                    2
                ),

            "Days Remaining":
                result["Days Remaining"],

            "Priority Score":
                round(
                    result["Priority Score"],
                    1
                ),

            "Priority":
                result["Priority"]
        })


    df = pd.DataFrame(
        table_data
    )


    st.dataframe(

        df,

        use_container_width=True,

        hide_index=True
    )


    # ========================================================
    # TOTAL DAILY STUDY
    # ========================================================

    total_daily = sum(

        result["Daily Hours"]

        for result in results
    )


    st.success(

        f"📚 Total planned study time: "
        f"**{total_daily:.2f} hours/day**"
    )


    # ========================================================
    # STUDY DASHBOARD
    # ========================================================

    st.header(
        "📊 Study Dashboard"
    )


    # --------------------------------------------------------
    # DAILY HOURS CHART
    # --------------------------------------------------------

    daily_chart = pd.DataFrame({

        "Subject": [

            result["Subject"]

            for result in results
        ],

        "Daily Hours": [

            result["Daily Hours"]

            for result in results
        ]
    })


    fig_daily = px.bar(

        daily_chart,

        x="Subject",

        y="Daily Hours",

        title="Daily Study Time by Subject",

        text_auto=".1f"
    )


    st.plotly_chart(

        fig_daily,

        use_container_width=True
    )


    # --------------------------------------------------------
    # TOTAL HOURS PIE
    # --------------------------------------------------------

    total_chart = pd.DataFrame({

        "Subject": [

            result["Subject"]

            for result in results
        ],

        "Total Hours": [

            result["Study Hours"]

            for result in results
        ]
    })


    fig_total = px.pie(

        total_chart,

        names="Subject",

        values="Total Hours",

        title="Distribution of Total Study Hours"
    )


    st.plotly_chart(

        fig_total,

        use_container_width=True
    )


    # --------------------------------------------------------
    # PRIORITY CHART
    # --------------------------------------------------------

    priority_chart = pd.DataFrame({

        "Subject": [

            result["Subject"]

            for result in results
        ],

        "Priority Score": [

            result["Priority Score"]

            for result in results
        ]
    })


    fig_priority = px.bar(

        priority_chart,

        x="Subject",

        y="Priority Score",

        title="Subject Priority Score",

        text_auto=".1f"
    )


    st.plotly_chart(

        fig_priority,

        use_container_width=True
    )


    # ========================================================
    # FEATURE IMPORTANCE
    # ========================================================

    st.header(
        "🔍 What Influences Your Study Plan?"
    )


    st.write(

        "These values show the relative importance "
        "of each feature in the Random Forest model."
    )


    fig_importance = px.bar(

        importance_data,

        x="Importance",

        y="Feature",

        orientation="h",

        title="Random Forest Feature Importance",

        text_auto=".3f"
    )


    fig_importance.update_layout(

        yaxis={
            "categoryorder":
                "total ascending"
        }
    )


    st.plotly_chart(

        fig_importance,

        use_container_width=True
    )


    # ========================================================
    # ADAPTIVE FEEDBACK
    # ========================================================

    st.header(
        "🔄 Adaptive Learning Feedback"
    )


    st.write(

        "Enter your recent performance. "
        "StudyWise compares your actual study time "
        "and quiz performance with the recommendation."
    )


    feedback_subject = st.selectbox(

        "📚 Select Subject",

        [

            result["Subject"]

            for result in results
        ],

        key="feedback_subject"
    )


    selected_result = next(

        (

            result

            for result in results

            if result["Subject"]
            == feedback_subject
        ),

        None
    )


    if selected_result:

        recommended_daily_hours = (

            selected_result["Daily Hours"]
        )


        st.info(

            f"Recommended daily study time for "
            f"**{feedback_subject}**: "
            f"**{recommended_daily_hours:.2f} hours**"
        )


        actual_study_hours = st.number_input(

            "⏱️ Actual Study Hours Today",

            min_value=0.0,

            max_value=10.0,

            value=min(
                2.0,
                float(
                    recommended_daily_hours
                )
            ),

            step=0.5,

            key="actual_study_hours"
        )


        quiz_score = st.slider(

            "📝 Latest Quiz Score",

            min_value=0,

            max_value=100,

            value=60,

            key="quiz_score"
        )


        if st.button(
            "🔄 Update My Priority"
        ):

            # ------------------------------------------------
            # OLD SCORE
            # ------------------------------------------------

            old_score = (
                selected_result[
                    "Priority Score"
                ]
            )


            # ------------------------------------------------
            # NEW SCORE
            # ------------------------------------------------

            new_score, new_priority, completion = (

                update_priority(

                    old_score,

                    quiz_score,

                    recommended_daily_hours,

                    actual_study_hours
                )
            )


            # ------------------------------------------------
            # FEEDBACK
            # ------------------------------------------------

            feedback_messages = (

                generate_feedback(

                    quiz_score,

                    recommended_daily_hours,

                    actual_study_hours
                )
            )


            # ------------------------------------------------
            # UPDATE MAIN PLAN
            # ------------------------------------------------

            selected_result[
                "Priority Score"
            ] = new_score


            selected_result[
                "Priority"
            ] = new_priority


            # ------------------------------------------------
            # SAVE PLAN
            # ------------------------------------------------

            st.session_state.results = results


            # ------------------------------------------------
            # SAVE FEEDBACK
            # ------------------------------------------------

            st.session_state.feedback_result = {

                "subject":
                    feedback_subject,

                "old_score":
                    old_score,

                "new_score":
                    new_score,

                "priority":
                    new_priority,

                "completion":
                    completion,

                "messages":
                    feedback_messages
            }


    # ========================================================
    # FEEDBACK RESULT
    # ========================================================

    if st.session_state.feedback_result:

        feedback = (
            st.session_state.feedback_result
        )


        st.subheader(

            f"📚 Updated Result — "
            f"{feedback['subject']}"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            st.metric(

                "Previous Score",

                f"{feedback['old_score']:.1f}"
            )


        with col2:

            st.metric(

                "Updated Score",

                f"{feedback['new_score']:.1f}",

                delta=round(

                    feedback["new_score"]
                    -
                    feedback["old_score"],

                    1
                )
            )


        with col3:

            st.metric(

                "Study Completion",

                f"{feedback['completion']:.1f}%"
            )


        st.success(

            f"Updated Priority: "
            f"**{feedback['priority']}**"
        )


        # ====================================================
        # FEEDBACK MESSAGES
        # ====================================================

        st.subheader(
            "💡 StudyWise Feedback"
        )


        for message in feedback["messages"]:

            st.write(
                f"• {message}"
            )


        # ====================================================
        # PRIORITY RECOMMENDATION
        # ====================================================

        if feedback["priority"] == "🔴 HIGH":

            st.warning(

                "StudyWise recommends giving this "
                "subject additional attention and "
                "reviewing your weak topics."
            )


        elif feedback["priority"] == "🟡 MEDIUM":

            st.info(

                "Keep practicing this subject "
                "consistently and monitor your "
                "quiz performance."
            )


        else:

            st.success(

                "Your current performance is relatively "
                "stable. Continue maintaining your progress."
            )