import streamlit as st
import os

from utils.rag_utils import load_vector_store, create_vector_store
from utils.document_loader import load_documents
from utils.agent_graph import build_agent

# -------------------------
# PAGE CONFIG
# -------------------------

st.set_page_config(page_title="HeritageGuide AI", layout="wide")

st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0E1117;
}

/* Chat container width */
.block-container {
    max-width: 900px;
}

/* User message bubble */
[data-testid="stChatMessage"]:has(.avatar-user) {
    background-color: #1E1E2E;
    border-radius: 12px;
    padding: 12px;
}

/* Assistant message bubble */
[data-testid="stChatMessage"]:has(.avatar-assistant) {
    background-color: #111827;
    border-radius: 12px;
    padding: 12px;
}

/* Chat input styling */
[data-testid="stChatInput"] textarea {
    border-radius: 12px;
}

/* Sidebar style */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

st.markdown(
"""
<h1 style='text-align: center;'>
🏛️ Heritage Guide
</h1>

<p style='text-align: center; color: grey;'>
Your intelligent guide to Indian heritage sites
</p>
""",
unsafe_allow_html=True
)

# -------------------------
# LOAD SYSTEM (CACHE)
# -------------------------

@st.cache_resource(show_spinner=False)
def load_system():
    """
    Load heavy resources only once:
    - Agent
    - Vector DB
    """
    vectordb = load_vector_store()
    agent = build_agent()

    return agent, vectordb


agent, vectordb = load_system()

# -------------------------
# SIDEBAR
# -------------------------

st.sidebar.markdown("## ⚙️ Settings")

# Response Mode
mode = st.sidebar.radio(
    "Response Mode",
    ["Concise", "Detailed"]
)

st.session_state["mode"] = mode
st.sidebar.divider()

# -------------------------
# LIST SITES IN KNOWLEDGE BASE
# -------------------------

st.sidebar.markdown("### 📚 Knowledge Base")

folders = ["knowledge_base", "uploads"]

sites = []

for folder in folders:

    if os.path.exists(folder):

        files = os.listdir(folder)

        sites.extend([
            f.replace(".pdf", "")
            for f in files
            if f.endswith(".pdf")
        ])

if sites:

    for site in sites:
        st.sidebar.write(f"📄 {site}")

else:
    st.sidebar.write("No knowledge base found")

st.sidebar.divider()
# -------------------------
# UPLOAD DOCUMENT
# -------------------------

st.sidebar.markdown("### 📤 Upload New Site")

uploaded_file = st.sidebar.file_uploader(
    "Upload PDF",
    type="pdf"
)

if uploaded_file:

    os.makedirs("uploads", exist_ok=True)

    path = os.path.join("uploads", uploaded_file.name)

    with open(path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    docs = load_documents("uploads")

    create_vector_store(docs)

    # Clear cached system so new vector DB loads
    st.cache_resource.clear()

    st.sidebar.success("Document added to knowledge base! Please refresh.")

# -------------------------
# CHAT MEMORY
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# DISPLAY CHAT HISTORY
# -------------------------

for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -------------------------
# CHAT INPUT
# -------------------------

user_input = st.chat_input("Ask about Indian heritage sites...")

if user_input:

    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    # -------------------------
    # AGENT CALL
    # -------------------------

    with st.spinner("🧠 HeritageGuide AI is thinking..."):

        result = agent.invoke(
            {
                "messages": [("user", user_input)],
                "mode": mode
            }
        )

        message = result["messages"][-1].content
        sources = result.get("sources", [])

        # Gemini sometimes returns structured content
        if isinstance(message, list):
            response = message[0]["text"]
        else:
            response = message

    # -------------------------
    # RESPONSE MODE CONTROL
    # -------------------------

    if mode == "Concise":
        response = response[:400]

    # Display response
    with st.chat_message("assistant"):

        st.markdown(response)

        if sources:
            with st.expander("📄 Sources"):
                for s in sources:
                    name = s.split("/")[-1]
                    st.write("•", name)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )