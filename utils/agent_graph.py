import streamlit as st

from utils.rag_utils import load_vector_store
from utils.web_search import search_web
from models.llm import load_agent_llm
from langchain_core.messages import AIMessage


vectordb = None
llm = None


# -------------------------
# RAG ANSWER
# -------------------------

def rag_answer(question):

    global vectordb, llm

    mode = st.session_state.get("mode", "Concise")

    # Better retriever (MMR)
    retriever = vectordb.as_retriever(
        search_type="mmr",
        search_kwargs={
            "k": 3,
            "fetch_k": 15
        }
    )

    docs = retriever.invoke(question)

    # -------------------------
    # Prefer documents whose name matches the query
    # -------------------------

    filtered_docs = []

    question_words = question.lower().split()

    for doc in docs:

        source = doc.metadata.get("source", "").lower()

        if any(word in source for word in question_words):
            filtered_docs.append(doc)

    if filtered_docs:
        docs = filtered_docs

    # -------------------------
    # Build context
    # -------------------------

    context = "\n".join([doc.page_content for doc in docs])

    sources = list(set(
        doc.metadata.get("source", "Unknown")
        for doc in docs
    ))

    prompt = f"""
You are an expert historian and heritage guide for Indian monuments.

Use ONLY the provided context to answer.

Context:
{context}

User Question:
{question}

Response Mode: {mode}

If mode is Concise:
Answer in 2–3 sentences.

If mode is Detailed:
Write structured sections:

History
Architecture
Cultural Importance
Interesting Facts

If the context does not contain the answer, say:
"I do not have information about this site in the knowledge base."
"""

    response = llm.invoke(prompt)

    return response.content, sources


# -------------------------
# TOURISM ANSWER
# -------------------------

def tourism_answer(question):

    global llm

    mode = st.session_state.get("mode", "Concise")

    web_results = search_web(question)

    prompt = f"""
Use the web information to answer the tourism question.

Web Information:
{web_results}

Question:
{question}

Response Mode: {mode}

If mode is Concise:
Give a short answer.

If mode is Detailed:
Provide:

Ticket Prices
Opening Timings
Best Time to Visit
Nearest Airport / Railway Station
Travel Tips
"""

    response = llm.invoke(prompt)

    return response.content


# -------------------------
# SIMPLE ROUTER
# -------------------------

def route_question(question):

    tourism_keywords = [
        "ticket",
        "price",
        "timing",
        "open",
        "close",
        "weather",
        "airport",
        "railway",
        "how to reach",
        "travel",
        "visit"
    ]

    for word in tourism_keywords:
        if word in question.lower():
            return tourism_answer(question)

    return rag_answer(question)


# -------------------------
# AGENT WRAPPER
# -------------------------

class HeritageAgent:

    def invoke(self, data):

        question = data["messages"][-1][1]

        result = route_question(question)

        if isinstance(result, tuple):
            answer, sources = result
        else:
            answer = result
            sources = ["Live Web Search"]

        return {
            "messages": [AIMessage(content=answer)],
            "sources": sources
        }


# -------------------------
# BUILD AGENT
# -------------------------

def build_agent():

    global vectordb, llm

    vectordb = load_vector_store()
    llm = load_agent_llm()

    return HeritageAgent()