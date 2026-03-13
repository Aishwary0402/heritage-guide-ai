from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query):

    results = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    text_results = []

    for r in results["results"]:
        text_results.append(r["content"])

    return "\n".join(text_results)