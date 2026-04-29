import os
from langchain.tools import Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

def get_search_tool() -> Tool:
    """
    External tool: searches the web using Tavily API.
    Get your free key at: https://tavily.com
    """
    tavily = TavilySearchResults(
        max_results=3,
        api_key=os.getenv("TAVILY_API_KEY")
    )

    return Tool(
        name="search_web",
        func=tavily.run,
        description=(
            "Useful for searching the internet for recent information, news, "
            "definitions, or any topic that requires up-to-date knowledge. "
            "Input should be a clear search query string."
        )
    )