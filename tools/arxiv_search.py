import arxiv
from langchain.tools import Tool

def get_arxiv_tool() -> Tool:
    """
    External tool: searches academic papers on arxiv.org.
    Completely free — no API key required.
    """

    def search_arxiv(query: str) -> str:
        try:
            client = arxiv.Client()
            search = arxiv.Search(
                query=query,
                max_results=3,
                sort_by=arxiv.SortCriterion.Relevance
            )
            results = list(client.results(search))

            if not results:
                return "No papers found for this query."

            output = []
            for paper in results:
                output.append(
                    f"**Title**: {paper.title}\n"
                    f"**Authors**: {', '.join(a.name for a in paper.authors[:3])}\n"
                    f"**Published**: {paper.published.strftime('%Y-%m-%d')}\n"
                    f"**Summary**: {paper.summary[:300]}...\n"
                    f"**Link**: {paper.entry_id}\n"
                )
            return "\n---\n".join(output)

        except Exception as e:
            return f"ArXiv search failed: {str(e)}"

    return Tool(
        name="search_arxiv",
        func=search_arxiv,
        description=(
            "Useful for finding academic research papers on a topic. "
            "Input should be a research topic or keywords. "
            "Returns paper titles, authors, summaries, and links from arxiv.org."
        )
    )