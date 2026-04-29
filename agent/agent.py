import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub

from agent.prompts import SYSTEM_PROMPT
from tools.search import get_search_tool
from tools.summarize import get_summarize_tool
from tools.calculator import get_calculator_tool
from tools.arxiv_search import get_arxiv_tool

load_dotenv()

def create_agent():
    # 1. LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3,
    )

    # 2. Tools
    tools = [
        get_search_tool(),
        get_summarize_tool(llm),
        get_calculator_tool(),
        get_arxiv_tool(),
    ]

    # 3. ReAct prompt
    prompt = hub.pull("hwchase17/react-chat")

    # 4. Agent
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    # 5. Executor (no memory — avoids version conflicts)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )

    return agent_executor


def run_agent(agent_executor, user_input: str) -> str:
    try:
        response = agent_executor.invoke({"input": user_input, "chat_history": []})
        return response["output"]
    except Exception as e:
        return f"An error occurred: {str(e)}"