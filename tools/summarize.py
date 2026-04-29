from langchain.tools import Tool
from langchain.schema import HumanMessage

def get_summarize_tool(llm) -> Tool:
    """
    Internal tool: summarizes a long text using the LLM directly.
    No external API needed.
    """

    def summarize(text: str) -> str:
        if len(text.strip()) < 100:
            return "Text is too short to summarize."
        try:
            prompt = f"Please summarize the following text clearly and concisely:\n\n{text}"
            response = llm.invoke([HumanMessage(content=prompt)])
            return response.content
        except Exception as e:
            return f"Summarization failed: {str(e)}"

    return Tool(
        name="summarize_text",
        func=summarize,
        description=(
            "Useful for summarizing long pieces of text. "
            "Input should be the full text you want summarized. "
            "Returns a concise summary."
        )
    )