from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from config.config import (
    GEMINI_API_KEY,
    GROK_API_KEY,
    GEMINI_MODEL,
    GROK_MODEL
)


def load_agent_llm():

    gemini = ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GEMINI_API_KEY,
        temperature=0.2
    )

    groq = ChatGroq(
        model=GROK_MODEL,
        api_key=GROK_API_KEY,
        temperature=0.2
    )

    # Native fallback support
    llm = gemini.with_fallbacks([groq])

    return llm


def load_tool_llm():

    return ChatGroq(
        model=GROK_MODEL,
        api_key=GROK_API_KEY,
        temperature=0.2
    )