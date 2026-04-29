"""
Run with: python -m tests.test_tools
Tests each tool independently before plugging into the agent.
"""
from tools.calculator import get_calculator_tool
from tools.arxiv_search import get_arxiv_tool

def test_calculator():
    print("Testing calculator...")
    tool = get_calculator_tool()
    assert "4" in tool.run("2 + 2")
    assert "25.0" in tool.run("(10 * 5) / 2")
    assert "Error" in tool.run("10 / 0")
    print("  Calculator: OK")

def test_arxiv():
    print("Testing arxiv search...")
    tool = get_arxiv_tool()
    result = tool.run("transformer neural network attention")
    assert "Title" in result
    print("  ArXiv: OK")
    print(f"  Sample result:\n{result[:300]}...")

if __name__ == "__main__":
    test_calculator()
    test_arxiv()
    print("\nAll tests passed!")