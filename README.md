# 📚 StudyWise — AI-Powered Personalized Study Planner

StudyWise is a web-based AI study planning application that creates personalized study recommendations based on a student's academic performance, subject difficulty, confidence level, preparation time, and previous study behavior.

The system combines Machine Learning, NLP, rule-based prioritization, study-time allocation, and adaptive feedback into one application.

---

## 🌐 Live Demo

👉 [Open StudyWise](https://studywise-va69.onrender.com)
---

## 🎯 Problem Statement

Students often study all subjects for the same amount of time even though their academic needs are different.

StudyWise attempts to solve this problem by analyzing multiple student-related factors and generating a personalized study plan.

The system answers questions such as:

- How many hours should I study?
- Which subject needs more attention?
- Which topics appear to be weak?
- How should my available daily time be divided?
- How should my priority change after a quiz?

---

## ✨ Features

### 🤖 Machine Learning Study Prediction

A Random Forest Regressor predicts recommended study hours using:

- Previous marks
- Current marks
- Subject difficulty
- Days remaining
- Confidence level
- Previous study hours
- Available daily hours

---

### 📚 Multi-Subject Planning

Students can select multiple subjects such as:

- Python
- Machine Learning
- DBMS
- Operating Systems
- Computer Networks
- Java

The application generates recommendations for each selected subject.

---

### 🧠 NLP Weak Topic Detection

StudyWise analyzes the student's description of difficult topics and detects known subject/topic keywords.

For example:

> "I struggle with DBMS joins and normalization."

The system can identify:

- DBMS → joins
- DBMS → normalization

---

### 🎯 Priority Engine

A rule-based priority score is calculated using:

- Current marks
- Difficulty
- Confidence
- Detected weak topics

Subjects can then receive:

- 🔴 HIGH
- 🟡 MEDIUM
- 🟢 LOW

priority.

---

### ⏱️ Study Time Allocation

The predicted study requirements are converted into a daily schedule based on the student's available study time.

Example:

```text
Available daily time: 3 hours

Machine Learning → 1.4h
DBMS             → 0.9h
Python           → 0.7h