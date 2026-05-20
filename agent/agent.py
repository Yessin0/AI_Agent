import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_react_agent, AgentExecutor
from langchain import hub
from langchain.callbacks.base import BaseCallbackHandler

from agent.prompts import SYSTEM_PROMPT
from tools.search import get_search_tool
from tools.summarize import get_summarize_tool
from tools.calculator import get_calculator_tool
from tools.arxiv_search import get_arxiv_tool

load_dotenv()

# ── Custom callback to capture reasoning steps ────────────────────────────────
class ReasoningCallback(BaseCallbackHandler):
    def __init__(self):
        self.steps = []

    def on_agent_action(self, action, **kwargs):
        self.steps.append({
            "type": "action",
            "thought": action.log.strip(),
            "tool": action.tool,
            "input": str(action.tool_input),
        })

    def on_tool_end(self, output, **kwargs):
        if self.steps and self.steps[-1]["type"] == "action":
            self.steps[-1]["observation"] = str(output)[:300]

    def reset(self):
        self.steps = []


def create_agent():
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0.3,
    )

    tools = [
        get_search_tool(),
        get_summarize_tool(llm),
        get_calculator_tool(),
        get_arxiv_tool(),
    ]

    prompt = hub.pull("hwchase17/react-chat")
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)

    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
    )

    return agent_executor


def run_agent(agent_executor, user_input: str):
    """
    Returns (final_answer, reasoning_steps)
    """
    callback = ReasoningCallback()
    try:
        response = agent_executor.invoke(
            {"input": user_input, "chat_history": []},
            config={"callbacks": [callback]}
        )
        return response["output"], callback.steps
    except Exception as e:
        return f"An error occurred: {str(e)}", []