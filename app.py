import streamlit as st

# ---------------------------------
# MOOD CHECKER - STREAMLIT EDITION
# ---------------------------------

st.set_page_config(
    page_title="Mood Check",
    page_icon="😊",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Modern styling
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f4f7ff, #f9fbff);
    }

    .block-container {
        max-width: 850px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(135deg, #4f6bed, #7c6cf2);
        color: white;
        padding: 30px;
        border-radius: 22px;
        margin-bottom: 24px;
    }

    .hero h1 {
        color: white;
        font-size: 2.4rem;
        margin-bottom: 8px;
    }

    .hero p {
        color: #eef0ff;
        font-size: 1.05rem;
    }

    .question-card {
        background: white;
        padding: 24px;
        border-radius: 18px;
        border: 1px solid #e1e8f5;
        margin: 15px 0;
    }

    .result-card {
        background: white;
        padding: 26px;
        border-radius: 20px;
        border: 1px solid #e1e8f5;
        margin-top: 18px;
    }

    div.stButton > button {
        border-radius: 12px;
        min-height: 45px;
        font-weight: 600;
        width: 100%;
    }

    div[data-testid="stRadio"] label {
        padding: 5px 0;
    }

    .small-note {
        color: #68758f;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)


QUESTIONS = [
    {
        "question": "How would you describe your mood today?",
        "options": [
            ("😊", "Very happy", 4),
            ("🙂", "Mostly happy", 3),
            ("😐", "Neutral", 2),
            ("😔", "A little down", 1),
            ("😢", "Very sad", 0),
        ],
    },
    {
        "question": "How energetic do you feel?",
        "options": [
            ("⚡", "Full of energy", 4),
            ("🌞", "Quite energetic", 3),
            ("🌤️", "Average energy", 2),
            ("🥱", "Rather tired", 1),
            ("😴", "Completely exhausted", 0),
        ],
    },
    {
        "question": "How well did you sleep recently?",
        "options": [
            ("🌙", "Very well", 4),
            ("😌", "Fairly well", 3),
            ("😐", "It was okay", 2),
            ("🥱", "Not very well", 1),
            ("😵", "Barely slept", 0),
        ],
    },
    {
        "question": "How stressed do you feel?",
        "options": [
            ("🧘", "Not stressed", 4),
            ("🌿", "A little stressed", 3),
            ("😐", "Moderately stressed", 2),
            ("😟", "Very stressed", 1),
            ("😣", "Overwhelmed", 0),
        ],
    },
    {
        "question": "How motivated are you to do things?",
        "options": [
            ("🚀", "Very motivated", 4),
            ("💪", "Fairly motivated", 3),
            ("🙂", "Somewhat motivated", 2),
            ("😕", "Not very motivated", 1),
            ("🛌", "No motivation today", 0),
        ],
    },
    {
        "question": "How connected do you feel to others?",
        "options": [
            ("❤️", "Very connected", 4),
            ("🤗", "Well supported", 3),
            ("🙂", "Neither connected nor alone", 2),
            ("🌧️", "A little lonely", 1),
            ("💙", "Very lonely", 0),
        ],
    },
    {
        "question": "How well are you managing daily tasks?",
        "options": [
            ("🌟", "Very well", 4),
            ("✅", "Pretty well", 3),
            ("📝", "Managing okay", 2),
            ("⏳", "Finding it difficult", 1),
            ("🌊", "Feeling overwhelmed", 0),
        ],
    },
    {
        "question": "How hopeful do you feel about the coming days?",
        "options": [
            ("🌈", "Very hopeful", 4),
            ("☀️", "Mostly hopeful", 3),
            ("🌤️", "Unsure", 2),
            ("🌥️", "Not very hopeful", 1),
            ("🌧️", "Very discouraged", 0),
        ],
    },
]


# Initialize session state
if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = [None] * len(QUESTIONS)


def save_current_answer():
    """Save the selected option before changing questions."""
    i = st.session_state.question_index
    key = f"choice_{i}"
    if key in st.session_state:
        st.session_state.answers[i] = st.session_state[key]


def previous_question():
    save_current_answer()
    st.session_state.question_index -= 1


def restart_quiz():
    st.session_state.question_index = 0
    st.session_state.answers = [None] * len(QUESTIONS)

    # Clear old widget selections
    for i in range(len(QUESTIONS)):
        key = f"choice_{i}"
        if key in st.session_state:
            del st.session_state[key]


# Header
st.markdown("""
<div class="hero">
    <h1>😊 Mood Check</h1>
    <p>A few simple questions. A better understanding of your mood.</p>
    <p>Take a moment for yourself. Answer honestly, without judgment.</p>
</div>
""", unsafe_allow_html=True)


# Display the quiz
if st.session_state.question_index < len(QUESTIONS):
    i = st.session_state.question_index
    question = QUESTIONS[i]

    st.progress((i + 1) / len(QUESTIONS))
    st.caption(f"QUESTION {i + 1} OF {len(QUESTIONS)}")

    st.markdown(
        f'<div class="question-card"><h3>{question["question"]}</h3>'
        '<p class="small-note">Choose the answer that fits you best.</p></div>',
        unsafe_allow_html=True,
    )

    previous_answer = st.session_state.answers[i]

    st.radio(
        "Select one answer:",
        options=list(range(len(question["options"]))),
        format_func=lambda j: (
            f"{question['options'][j][0]}  "
            f"{question['options'][j][1]}"
        ),
        index=previous_answer,
        key=f"choice_{i}",
        label_visibility="collapsed",
    )

    st.write("")
    left, right = st.columns(2)

    with left:
        if i > 0:
            st.button(
                "← Back",
                on_click=previous_question,
                use_container_width=True,
            )

    with right:
        button_label = (
            "See My Results →"
            if i == len(QUESTIONS) - 1
            else "Next →"
        )

        if st.button(
            button_label,
            type="primary",
            use_container_width=True,
        ):
            save_current_answer()

            if st.session_state.answers[i] is None:
                st.warning("Please select an answer first.")
            elif i < len(QUESTIONS) - 1:
                st.session_state.question_index += 1
                st.rerun()
            else:
                st.session_state.question_index += 1
                st.rerun()

# Results
else:
    scores = [
        QUESTIONS[i]["options"][answer][2]
        for i, answer in enumerate(st.session_state.answers)
    ]

    total = sum(scores)
    maximum = len(QUESTIONS) * 4
    percentage = total / maximum * 100

    if percentage >= 80:
        emoji = "🌟"
        title = "You're feeling positive!"
        message = (
            "Your answers suggest a generally positive mood. "
            "Enjoy what is going well and make time for the things you value."
        )
        tips = [
            "Celebrate a small win today.",
            "Stay connected with people you enjoy.",
            "Make time for rest and activities you love.",
        ]
    elif percentage >= 60:
        emoji = "🙂"
        title = "You're doing fairly well"
        message = (
            "Your answers suggest a mostly okay mood, "
            "although some areas may need attention."
        )
        tips = [
            "Take a short break when you need one.",
            "Do something enjoyable for ten minutes.",
            "Balance your responsibilities with rest.",
        ]
    elif percentage >= 40:
        emoji = "🌿"
        title = "Time for a little self-care"
        message = (
            "Your answers suggest a mixed mood. Consider what may be "
            "draining you and what could help you feel more supported."
        )
        tips = [
            "Take a gentle walk or get some fresh air.",
            "Talk to someone you trust.",
            "Choose one small, manageable task.",
        ]
    else:
        emoji = "💙"
        title = "Be gentle with yourself"
        message = (
            "Your answers suggest you may be having a difficult time. "
            "You deserve care, patience, and support."
        )
        tips = [
            "Give yourself permission to rest.",
            "Reach out to someone you trust.",
            "Consider professional support if these feelings persist "
            "or affect daily life.",
        ]

    st.progress(1.0)
    st.caption("YOUR RESULTS")

    st.markdown(
        f"""
        <div class="result-card">
            <div style="font-size: 3rem; text-align: center;">{emoji}</div>
            <h2 style="text-align: center;">{title}</h2>
            <p style="text-align: center; color: #4f6bed; font-weight: bold;">
                Reflection score: {total}/{maximum}
            </p>
            <p style="text-align: center;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("🌱 A few things to try")
    for tip in tips:
        st.markdown(f"- {tip}")

    st.info(
        "This is a self-reflection tool, not a diagnosis. Your feelings "
        "can change, and one score cannot define your well-being."
    )

    st.button(
        "↻ Take the Quiz Again",
        on_click=restart_quiz,
        type="primary",
        use_container_width=True,
    )

st.divider()
st.markdown(
    "<p style='text-align:center; color:#68758f; font-size:0.85rem;'>"
    "Made with Python and Streamlit · Take care of yourself 💙"
    "</p>",
    unsafe_allow_html=True,
)
