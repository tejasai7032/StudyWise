# 📚 StudyWise — AI-Powered Personalized Study Planner

StudyWise is an AI-powered academic planning application that helps students create personalized study schedules based on their academic performance, subject difficulty, confidence level, available study time, and remaining preparation days.

The system combines:

- 🤖 Machine Learning
- 🧠 NLP-based weak-topic detection
- 📊 Rule-based priority scoring
- 🔄 Adaptive feedback
- 🗓️ Personalized timetable generation
- 📈 Interactive data visualization
- 🧪 Automated testing

---

# 🎯 Problem Statement

Students often struggle to decide:

- Which subject should receive more attention?
- How many hours should be spent studying?
- Which topics need revision?
- How should available study time be divided?
- How should the plan change after a poor or good quiz result?

StudyWise attempts to solve these problems by combining Machine Learning with rule-based recommendation logic and NLP-based topic detection.

---

# 💡 Solution

StudyWise takes student academic information as input and generates a personalized study plan.

The system:

1. Predicts recommended study hours using a Random Forest Regression model.
2. Calculates subject priority using academic and difficulty-related factors.
3. Detects weak topics using subject-aware NLP keyword detection.
4. Allocates available daily study time across subjects.
5. Generates a structured timetable with study sessions and breaks.
6. Collects quiz performance and actual study time.
7. Dynamically updates subject priority using adaptive feedback.
8. Displays the results through an interactive Streamlit dashboard.

---

# 🏗️ System Architecture

```text
                    Student
                       │
                       ▼
              Streamlit Input Form
                       │
             ┌─────────┼─────────┐
             │         │         │
             ▼         ▼         ▼
        ML Model      NLP      Priority
             │         │         │
             ▼         ▼         ▼
       Study Hours  Weak Topics  Score
             │         │         │
             └─────────┼─────────┘
                       │
                       ▼
              Recommendation Engine
                       │
                       ▼
             Daily Study Allocation
                       │
                       ▼
              Timetable Generator
                       │
                       ▼
               StudyWise Dashboard
                       │
                       ▼
              Quiz + Study Feedback
                       │
                       ▼
             Adaptive Priority Update