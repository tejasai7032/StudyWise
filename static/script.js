// ============================================================
// STUDYWISE — FRONTEND JAVASCRIPT
// ============================================================


let currentPlan = null;


// ============================================================
// ELEMENTS
// ============================================================

const subjectCheckboxes =
    document.querySelectorAll(
        ".subject-checkbox"
    );


const subjectCards =
    document.getElementById(
        "subjectCards"
    );


const generateButton =
    document.getElementById(
        "generateButton"
    );


// ============================================================
// SUBJECT EMOJIS
// ============================================================

function getSubjectEmoji(subject) {

    const emojis = {

        "Python": "🐍",

        "Machine Learning": "🤖",

        "DBMS": "🗄️",

        "Operating Systems": "💻",

        "Computer Networks": "🌐",

        "Java": "☕"

    };

    return emojis[subject] || "📚";
}


// ============================================================
// CREATE SUBJECT INPUT CARD
// ============================================================

function createSubjectCard(
    subject,
    index
) {

    const card =
        document.createElement(
            "div"
        );


    card.className =
        "glass-card subject-input-card";


    card.dataset.subject =
        subject;


    card.innerHTML = `

        <div class="subject-card-header">

            <div>

                <div class="subject-card-name">

                    ${getSubjectEmoji(subject)}

                    ${subject}

                </div>

                <div class="subject-card-subtitle">

                    Academic performance

                </div>

            </div>


            <span class="subject-number">

                ${index + 1}

            </span>

        </div>


        <div class="form-grid">


            <div class="form-group">

                <label>
                    Previous Marks
                </label>

                <input
                    type="number"
                    class="previous-marks"
                    min="0"
                    max="100"
                    value="60"
                >

            </div>


            <div class="form-group">

                <label>
                    Current Marks
                </label>

                <input
                    type="number"
                    class="current-marks"
                    min="0"
                    max="100"
                    value="62"
                >

            </div>


            <div class="form-group">

                <label>
                    Difficulty
                </label>

                <select class="difficulty">

                    <option value="1">
                        1 — Easy
                    </option>

                    <option value="2">
                        2
                    </option>

                    <option value="3" selected>
                        3 — Moderate
                    </option>

                    <option value="4">
                        4
                    </option>

                    <option value="5">
                        5 — Very Hard
                    </option>

                </select>

            </div>


            <div class="form-group">

                <label>
                    Confidence
                </label>

                <select class="confidence">

                    <option value="1">
                        1 — Very Low
                    </option>

                    <option value="2">
                        2
                    </option>

                    <option value="3" selected>
                        3 — Moderate
                    </option>

                    <option value="4">
                        4
                    </option>

                    <option value="5">
                        5 — Very High
                    </option>

                </select>

            </div>


            <div class="form-group">

                <label>
                    Days Remaining
                </label>

                <input
                    type="number"
                    class="days-remaining"
                    min="1"
                    value="25"
                >

            </div>


            <div class="form-group">

                <label>
                    Previous Study Hours
                </label>

                <input
                    type="number"
                    class="previous-study"
                    min="0"
                    step="0.5"
                    value="15"
                >

            </div>


        </div>

    `;


    subjectCards.appendChild(
        card
    );

}


// ============================================================
// UPDATE SUBJECT CARDS
// ============================================================

function updateSubjectCards() {

    const selectedSubjects =
        Array.from(
            subjectCheckboxes
        )
        .filter(
            checkbox =>
                checkbox.checked
        )
        .map(
            checkbox =>
                checkbox.value
        );


    subjectCards.innerHTML = "";


    selectedSubjects.forEach(
        (subject, index) => {

            createSubjectCard(
                subject,
                index
            );

        }
    );

}


subjectCheckboxes.forEach(
    checkbox => {

        checkbox.addEventListener(
            "change",
            updateSubjectCards
        );

    }
);


// Initial cards
updateSubjectCards();


// ============================================================
// THEME TOGGLE
// ============================================================

const themeToggle =
    document.getElementById(
        "themeToggle"
    );


if (themeToggle) {

    themeToggle.addEventListener(
        "click",
        () => {

            document.body.classList.toggle(
                "light-mode"
            );


            const light =
                document.body.classList.contains(
                    "light-mode"
                );


            themeToggle.textContent =
                light
                    ? "☀️"
                    : "🌙";

        }
    );

}


// ============================================================
// GENERATE PLAN
// ============================================================

generateButton.addEventListener(
    "click",
    generatePlan
);


async function generatePlan() {

    const cards =
        document.querySelectorAll(
            ".subject-input-card"
        );


    if (cards.length === 0) {

        alert(
            "Please select at least one subject."
        );

        return;

    }


    generateButton.disabled =
        true;


    generateButton.innerHTML =
        "🧠 Analyzing your subjects...";


    const subjects = [];


    cards.forEach(
        card => {

            subjects.push({

                name:
                    card.dataset.subject,

                previousMarks:
                    Number(
                        card.querySelector(
                            ".previous-marks"
                        ).value
                    ),

                currentMarks:
                    Number(
                        card.querySelector(
                            ".current-marks"
                        ).value
                    ),

                difficulty:
                    Number(
                        card.querySelector(
                            ".difficulty"
                        ).value
                    ),

                confidence:
                    Number(
                        card.querySelector(
                            ".confidence"
                        ).value
                    ),

                daysRemaining:
                    Number(
                        card.querySelector(
                            ".days-remaining"
                        ).value
                    ),

                previousStudy:
                    Number(
                        card.querySelector(
                            ".previous-study"
                        ).value
                    )

            });

        }
    );


    const availableHours =
        Number(
            document.getElementById(
                "availableHours"
            ).value
        );


    const weakTopics =
        document.getElementById(
            "weakTopics"
        ).value;


    try {

        const response =
            await fetch(
                "/generate-plan",
                {

                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body:
                        JSON.stringify({

                            subjects:
                                subjects,

                            availableHours:
                                availableHours,

                            weakTopics:
                                weakTopics

                        })

                }
            );


        const result =
            await response.json();


        if (
            !response.ok ||
            !result.success
        ) {

            throw new Error(
                result.error ||
                "Plan generation failed."
            );

        }


        currentPlan =
            result;


        renderSummary(
            result
        );


        renderResults(
            result
        );


        renderWeakTopics(
            result.detected_topics
        );


        renderTimetable(
            result
        );


        populateFeedbackSubjects(
            result
        );


        generateButton.innerHTML =
            "✓ Plan Generated Successfully";


        document
            .getElementById(
                "dashboard"
            )
            .scrollIntoView({
                behavior: "smooth"
            });


    } catch (error) {

        console.error(
            error
        );


        alert(
            "Unable to generate your plan.\n\n"
            + error.message
        );


        generateButton.innerHTML =
            "Try Again ✨";

    }


    setTimeout(
        () => {

            generateButton.disabled =
                false;


            generateButton.innerHTML =
                "Generate Personalized Plan ✨";

        },
        1800
    );

}


// ============================================================
// SUMMARY
// ============================================================

function renderSummary(
    result
) {

    document.getElementById(
        "totalRequired"
    ).textContent =
        `${result.total_required_hours.toFixed(1)}h`;


    document.getElementById(
        "totalDaily"
    ).textContent =
        `${result.total_daily_hours.toFixed(1)}h`;


    document.getElementById(
        "totalSubjects"
    ).textContent =
        result.subjects.length;


    document.getElementById(
        "totalWeakTopics"
    ).textContent =
        result.detected_topics.length;

}


// ============================================================
// RENDER RESULTS
// ============================================================

function renderResults(
    result
) {

    const container =
        document.getElementById(
            "resultsContainer"
        );


    if (
        !result.subjects ||
        result.subjects.length === 0
    ) {

        container.innerHTML = `

            <div class="empty-state">

                <div class="empty-icon">
                    📚
                </div>

                <h3>
                    No results available
                </h3>

                <p>
                    Please generate the plan again.
                </p>

            </div>

        `;

        return;

    }


    container.innerHTML = "";


    result.subjects.forEach(
        subject => {

            const card =
                document.createElement(
                    "div"
                );


            card.className =
                "result-card";


            const percentage =
                result.total_required_hours > 0

                    ? (
                        subject.study_hours
                        /
                        result.total_required_hours
                    ) * 100

                    : 0;


            card.innerHTML = `

                <div class="result-header">

                    <div>

                        <div class="result-subject">

                            ${getSubjectEmoji(
                                subject.subject
                            )}

                            ${subject.subject}

                        </div>


                        <div class="priority-badge">

                            ${subject.priority}

                        </div>

                    </div>


                    <div class="result-hours">

                        ${subject.study_hours}

                        <small>
                            hrs
                        </small>

                    </div>

                </div>


                <div class="result-metrics">


                    <div class="metric">

                        <span>
                            Daily Allocation
                        </span>

                        <strong>
                            ${subject.daily_hours}h
                        </strong>

                    </div>


                    <div class="metric">

                        <span>
                            Days Remaining
                        </span>

                        <strong>
                            ${subject.days_remaining}
                        </strong>

                    </div>


                    <div class="metric">

                        <span>
                            Priority Score
                        </span>

                        <strong>
                            ${subject.priority_score}/100
                        </strong>

                    </div>


                    <div class="metric">

                        <span>
                            NLP Weak Topic
                        </span>

                        <strong>
                            ${
                                subject.weak_topic
                                    ? "Detected"
                                    : "None"
                            }
                        </strong>

                    </div>


                </div>


                <div class="allocation">

                    <div class="allocation-label">

                        <span>
                            Required study share
                        </span>

                        <span>
                            ${percentage.toFixed(0)}%
                        </span>

                    </div>


                    <div class="allocation-track">

                        <div
                            class="allocation-fill"
                            style="
                                width: ${Math.max(
                                    percentage,
                                    3
                                )}%;
                            "
                        ></div>

                    </div>

                </div>

            `;


            container.appendChild(
                card
            );

        }
    );

}


// ============================================================
// RENDER WEAK TOPICS
// ============================================================

function renderWeakTopics(
    topics
) {

    const container =
        document.getElementById(
            "topicTags"
        );


    if (
        !topics ||
        topics.length === 0
    ) {

        container.innerHTML = `

            <span class="muted-message">

                No known weak topics detected.

            </span>

        `;

        return;

    }


    container.innerHTML = "";


    topics.forEach(
        item => {

            const tag =
                document.createElement(
                    "span"
                );


            tag.className =
                "topic-tag";


            tag.innerHTML = `

                <strong>
                    ${item.subject}
                </strong>

                ${item.topic}

            `;


            container.appendChild(
                tag
            );

        }
    );

}


// ============================================================
// TIMETABLE
// ============================================================

function renderTimetable(
    result
) {

    const timeline =
        document.getElementById(
            "timeline"
        );


    timeline.innerHTML = "";


    if (
        !result.subjects ||
        result.subjects.length === 0
    ) {

        timeline.innerHTML = `

            <div class="empty-state small">

                <p>
                    No timetable available.
                </p>

            </div>

        `;

        return;

    }


    const startTimeInput =
        document.getElementById(
            "startTime"
        ).value;


    let currentMinutes =
        timeToMinutes(
            startTimeInput
        );


    result.subjects.forEach(
        subject => {

            const dailyHours =
                Number(
                    subject.daily_hours
                );


            if (
                dailyHours <= 0
            ) {
                return;
            }


            const start =
                currentMinutes;


            const duration =
                dailyHours * 60;


            const end =
                currentMinutes
                + duration;


            createTimelineItem(
                timeline,
                subject,
                start,
                end
            );


            currentMinutes =
                end + 10;

        }
    );

}


// ============================================================
// CREATE TIMELINE ITEM
// ============================================================

function createTimelineItem(
    container,
    subject,
    start,
    end
) {

    const item =
        document.createElement(
            "div"
        );


    item.className =
        "timeline-item";


    item.innerHTML = `

        <div class="timeline-time">

            ${formatTime(start)}

            <br>

            ${formatTime(end)}

        </div>


        <div class="timeline-dot"></div>


        <div class="timeline-content">

            <strong>

                ${getSubjectEmoji(
                    subject.subject
                )}

                ${subject.subject}

            </strong>


            <span>

                ${subject.daily_hours} hours

                •

                ${subject.priority}

            </span>

        </div>

    `;


    container.appendChild(
        item
    );

}


// ============================================================
// TIME HELPERS
// ============================================================

function timeToMinutes(
    time
) {

    if (
        !time ||
        !time.includes(":")
    ) {

        return 9 * 60;

    }


    const parts =
        time.split(":");


    const hours =
        Number(parts[0]);


    const minutes =
        Number(parts[1]);


    return (
        hours * 60
        + minutes
    );

}


function formatTime(
    totalMinutes
) {

    totalMinutes =
        Math.round(
            totalMinutes
        );


    const hours =
        Math.floor(
            totalMinutes / 60
        ) % 24;


    const minutes =
        totalMinutes % 60;


    const suffix =
        hours >= 12
            ? "PM"
            : "AM";


    const displayHour =
        hours % 12 || 12;


    return `

        ${displayHour}:

        ${String(
            minutes
        ).padStart(
            2,
            "0"
        )}

        ${suffix}

    `;

}


// ============================================================
// FEEDBACK SUBJECTS
// ============================================================

function populateFeedbackSubjects(
    result
) {

    const select =
        document.getElementById(
            "feedbackSubject"
        );


    select.innerHTML = "";


    result.subjects.forEach(
        subject => {

            const option =
                document.createElement(
                    "option"
                );


            option.value =
                subject.subject;


            option.textContent =
                subject.subject;


            option.dataset.priority =
                subject.priority_score;


            option.dataset.hours =
                subject.daily_hours;


            select.appendChild(
                option
            );

        }
    );

}


// ============================================================
// FEEDBACK
// ============================================================

const feedbackButton =
    document.getElementById(
        "updateFeedbackButton"
    );


feedbackButton.addEventListener(
    "click",
    updateFeedback
);


async function updateFeedback() {

    if (!currentPlan) {

        alert(
            "Please generate a study plan first."
        );

        return;

    }


    const select =
        document.getElementById(
            "feedbackSubject"
        );


    if (!select.value) {

        alert(
            "Please select a subject."
        );

        return;

    }


    const selectedOption =
        select.options[
            select.selectedIndex
        ];


    const currentPriority =
        Number(
            selectedOption.dataset.priority
        );


    const recommendedHours =
        Number(
            selectedOption.dataset.hours
        );


    const actualHours =
        Number(
            document.getElementById(
                "actualHours"
            ).value
        );


    const quizScore =
        Number(
            document.getElementById(
                "quizScore"
            ).value
        );


    feedbackButton.disabled =
        true;


    feedbackButton.textContent =
        "Updating...";


    try {

        const response =
            await fetch(
                "/update-feedback",
                {

                    method: "POST",

                    headers: {

                        "Content-Type":
                            "application/json"

                    },

                    body:
                        JSON.stringify({

                            currentPriority:
                                currentPriority,

                            quizScore:
                                quizScore,

                            recommendedHours:
                                recommendedHours,

                            actualHours:
                                actualHours

                        })

                }
            );


        const result =
            await response.json();


        if (
            !response.ok ||
            !result.success
        ) {

            throw new Error(
                result.error ||
                "Feedback update failed."
            );

        }


        renderFeedback(
            result
        );


    } catch (error) {

        console.error(
            error
        );


        alert(
            "Unable to update feedback.\n\n"
            + error.message
        );

    }


    feedbackButton.disabled =
        false;


    feedbackButton.innerHTML =
        "Update Priority <span>↻</span>";

}


// ============================================================
// RENDER FEEDBACK
// ============================================================

function renderFeedback(
    result
) {

    const container =
        document.getElementById(
            "feedbackResult"
        );


    container.innerHTML = `

        <div class="feedback-result-inner">


            <div class="feedback-score">

                <div>

                    <div class="feedback-score-number">

                        ${result.new_score}

                    </div>

                    <div class="muted-message">
                        Updated priority score
                    </div>

                </div>


                <div>

                    <div class="priority-badge">

                        ${result.priority}

                    </div>

                    <div
                        class="muted-message"
                        style="margin-top:8px;"
                    >

                        Completion:
                        ${result.completion}%

                    </div>

                </div>

            </div>


            <div class="feedback-messages">

                ${result.messages
                    .map(
                        message => `

                            <div class="feedback-message">

                                💡 ${message}

                            </div>

                        `
                    )
                    .join("")
                }

            </div>

        </div>

    `;

}


// ============================================================
// SMOOTH SCROLL
// ============================================================

document
    .querySelectorAll(
        'a[href^="#"]'
    )
    .forEach(
        link => {

            link.addEventListener(
                "click",
                event => {

                    const targetId =
                        link.getAttribute(
                            "href"
                        );


                    const target =
                        document.querySelector(
                            targetId
                        );


                    if (target) {

                        event.preventDefault();


                        target.scrollIntoView({

                            behavior:
                                "smooth"

                        });

                    }

                }
            );

        }
    );


// ============================================================
// CONSOLE MESSAGE
// ============================================================

console.log(
    "📚 StudyWise frontend loaded successfully."
);

console.log(
    "🤖 ML + NLP + Adaptive Planning ready."
);