
# ROHITFKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk


import streamlit as st
from backend.Implementation import process_video, ask_question


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="YouTube AI Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# SESSION STATE
# =====================================================

if "retriever" not in st.session_state:
    st.session_state.retriever = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_url" not in st.session_state:
    st.session_state.video_url = ""

if "video_processed" not in st.session_state:
    st.session_state.video_processed = False


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #111111;
}

/* Main Content Width */
section.main > div {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #1c1c1c;
    min-width: 290px;
}

[data-testid="stSidebar"] h1 {
    font-size: 29px;
    font-weight: 800;
}

[data-testid="stSidebar"] h2 {
    font-size: 23px;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    font-size: 15px;
}

/* Main Header */
.header {
    text-align: center;
    padding: 10px 0 25px 0;
}

.header h1 {
    font-size: 42px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 10px;
}

.header p {
    font-size: 17px;
    color: #a5a5a5;
}

/* Section Headings */
h2, h3 {
    font-weight: 700;
}

/* Status */
.status {
    background-color: #1c2939;
    padding: 16px 20px;
    border-radius: 12px;
    border-left: 5px solid #20c997;
    font-size: 17px;
    margin-bottom: 15px;
}

/* Input Fields */
.stTextInput input {
    border-radius: 10px;
    min-height: 48px;
    font-size: 16px;
}

/* Buttons */
.stButton button,
.stFormSubmitButton button {
    min-height: 46px;
    border-radius: 10px;
    font-size: 15px;
    font-weight: 650;
}

/* Chat Messages */
[data-testid="stChatMessage"] {
    background-color: #1d1d1f;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 15px;
    width: 100%;
}

/* Chat Text */
[data-testid="stChatMessage"] p {
    font-size: 16px;
    line-height: 1.7;
}

/* Question Input Area */
.question-area {
    background-color: #202124;
    padding: 16px 18px 5px 18px;
    border-radius: 14px;
    border: 1px solid #383838;
    margin-top: 15px;
    margin-bottom: 25px;
}

/* Welcome Card */
.welcome-card {
    background-color: #1d1d1f;
    border: 1px solid #383838;
    padding: 25px;
    border-radius: 15px;
    margin-top: 25px;
}

.welcome-card p {
    font-size: 16px;
    color: #c5c5c5;
    line-height: 1.8;
}

/* Footer */
.footer {
    text-align: center;
    color: #777777;
    font-size: 14px;
    padding: 25px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("🎬 YouTube AI")

    st.caption("Your personal video assistant")

    st.divider()

    st.subheader("📹 Video Configuration")

    video_url = st.text_input(
        "YouTube Video URL",
        value=st.session_state.video_url,
        placeholder="Paste your YouTube link here..."
    )

    if st.button(
        "⚡ Process Video",
        use_container_width=True,
        type="primary"
    ):

        if video_url.strip():

            try:

                with st.spinner("Processing your video..."):

                    retriever = process_video(video_url.strip())

                    st.session_state.retriever = retriever

                    st.session_state.video_url = video_url.strip()

                    st.session_state.video_processed = True

                    st.session_state.messages = []

                st.success("Video processed successfully!")

                st.rerun()

            except Exception as e:

                st.error(f"Processing Error: {e}")

        else:

            st.warning("Please enter a YouTube URL.")

    st.divider()

    # Video Status

    if st.session_state.video_processed:

        st.success("🟢 Video Ready")

        st.markdown("**Current Video**")

        st.code(
            st.session_state.video_url,
            language=None
        )

        st.divider()

        # Clear Chat

        if st.button(
            "🗑️ Clear Chat",
            use_container_width=True
        ):

            st.session_state.messages = []

            st.rerun()

        # Reset Video

        if st.button(
            "🔄 Reset Video",
            use_container_width=True
        ):

            st.session_state.retriever = None

            st.session_state.video_url = ""

            st.session_state.video_processed = False

            st.session_state.messages = []

            st.rerun()

    else:

        st.info("Paste a YouTube link to get started.")

        st.markdown("""
        ### 🚀 How it works

        1. Paste your video URL.
        2. Process the video.
        3. Ask your questions.
        4. Get AI-powered answers.
        """)


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown("""
<div class="header">

    <h1>🎬 YouTube AI Assistant</h1>

    <p>
        Your personal AI assistant to understand,
        explore and learn from any YouTube video.
    </p>

</div>
""", unsafe_allow_html=True)


# =====================================================
# MAIN APPLICATION
# =====================================================

if not st.session_state.video_processed:

    st.markdown("""
    <div class="welcome-card">

        <h2>👋 Welcome to YouTube AI Assistant</h2>

        <p>
        Turn any YouTube video into an interactive
        learning experience.

        Ask questions, understand complex concepts,
        extract important information and learn faster
        with AI.
        </p>

        <h3>✨ What can you do?</h3>

        <p>
        📖 Get video summaries<br>
        ❓ Ask questions about video content<br>
        🧠 Understand difficult topics<br>
        🔍 Find specific information<br>
        📝 Generate notes from videos
        </p>

        <p>
        👈 Start by adding a YouTube URL in the sidebar.
        </p>

    </div>
    """, unsafe_allow_html=True)


else:

    # -----------------------------------------------
    # VIDEO STATUS
    # -----------------------------------------------

    st.markdown("""
    <div class="status">
        🟢 <b>Video Connected</b> &nbsp; | &nbsp;
        Ready to answer your questions
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------
    # QUESTION INPUT AT TOP
    # -----------------------------------------------

    st.markdown("### 💬 Ask Your Video Anything")

    with st.container():

        st.markdown(
            '<div class="question-area">',
            unsafe_allow_html=True
        )

        with st.form(
            "question_form",
            clear_on_submit=True
        ):

            col1, col2 = st.columns([5, 1])

            with col1:

                prompt = st.text_input(
                    "Your Question",
                    placeholder="Ask anything about this YouTube video...",
                    label_visibility="collapsed"
                )

            with col2:

                submitted = st.form_submit_button(
                    "➤ Send",
                    use_container_width=True,
                    type="primary"
                )

        st.markdown("</div>", unsafe_allow_html=True)

    # -----------------------------------------------
    # PROCESS QUESTION
    # -----------------------------------------------

    if submitted and prompt.strip():

        # Save user message

        st.session_state.messages.append({
            "role": "user",
            "content": prompt.strip()
        })

        try:

            with st.spinner("🤖 AI is thinking..."):

                response = ask_question(
                    prompt.strip(),
                    st.session_state.retriever
                )

            # Save assistant response

            st.session_state.messages.append({
                "role": "assistant",
                "content": response
            })

            st.rerun()

        except Exception as e:

            st.error(f"Error generating answer: {e}")

    # -----------------------------------------------
    # CHAT HISTORY
    # -----------------------------------------------

    st.divider()

    st.markdown("### 💬 Conversation")

    if not st.session_state.messages:

        st.info(
            "No questions yet. Start by asking something "
            "about your YouTube video!"
        )

    else:

        for message in st.session_state.messages:

            with st.chat_message(message["role"]):

                st.markdown(message["content"])


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown("""
<div class="footer">

    Built with ❤️ using Streamlit

    <br>

    YouTube RAG Assistant | AI Powered Learning

</div>
""", unsafe_allow_html=True)

