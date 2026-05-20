import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from agent.agent import create_agent, run_agent

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Academic Research Agent",
    page_icon="🔬",
    layout="wide",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Mono', monospace;
    background-color: #0d0d0d;
    color: #e8e8e0;
}
.main { background-color: #0d0d0d; }

h1 {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    letter-spacing: -0.03em;
    color: #f0e96a;
}
.subtitle {
    font-size: 0.85rem;
    color: #888;
    margin-top: -10px;
    margin-bottom: 30px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.tool-badge {
    display: inline-block;
    background: #1a1a1a;
    border: 1px solid #333;
    border-radius: 4px;
    padding: 3px 10px;
    font-size: 0.75rem;
    color: #f0e96a;
    margin: 3px;
    letter-spacing: 0.05em;
}
.chat-user {
    background: #1a1a1a;
    border-left: 3px solid #f0e96a;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
    font-size: 0.9rem;
}
.chat-agent {
    background: #111;
    border-left: 3px solid #444;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin: 10px 0;
    font-size: 0.9rem;
    color: #c8c8c0;
}
.label { font-size: 0.7rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 4px; }
.label-user { color: #f0e96a; }
.label-agent { color: #888; }
.step-box {
    background: #0a0a0a;
    border: 1px solid #2a2a2a;
    border-radius: 6px;
    padding: 10px 14px;
    margin: 6px 0;
    font-size: 0.8rem;
}
.step-thought { color: #aaa; }
.step-tool { color: #f0e96a; font-weight: bold; }
.step-obs { color: #7ec8a0; }

div[data-testid="stTextInput"] input {
    background: #1a1a1a !important;
    border: 1px solid #333 !important;
    color: #e8e8e0 !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.9rem !important;
}
div[data-testid="stButton"] button {
    background: #f0e96a !important;
    color: #0d0d0d !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 6px !important;
    padding: 0.5rem 1.5rem !important;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1>Research Agent</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Groq · LangChain · Multi-Tool AI</p>', unsafe_allow_html=True)
st.markdown("""
<span class="tool-badge">🔍 Web Search</span>
<span class="tool-badge">📄 Summarizer</span>
<span class="tool-badge">🧮 Calculator</span>
<span class="tool-badge">📚 ArXiv Papers</span>
""", unsafe_allow_html=True)
st.markdown("---")

# ── Session state ─────────────────────────────────────────────────────────────
if "agent" not in st.session_state:
    with st.spinner("Initializing agent..."):
        st.session_state.agent = create_agent()

if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class="chat-user">
            <div class="label label-user">You</div>
            {msg["content"]}
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="chat-agent">
            <div class="label label-agent">Agent</div>
            {msg["content"]}
        </div>""", unsafe_allow_html=True)

        # Show reasoning steps if any
        if msg.get("steps"):
            with st.expander(f"🧠 Agent Reasoning — {len(msg['steps'])} step(s)"):
                for i, step in enumerate(msg["steps"], 1):
                    st.markdown(f"**Step {i}**")
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        st.markdown(f"🔧 **Tool used:** `{step['tool']}`")
                        st.markdown(f"📥 **Input:** `{step['input']}`")
                    with col2:
                        # Show only the Thought line from the log
                        thought_lines = [
                            l for l in step["thought"].split("\n")
                            if l.strip().startswith("Thought:")
                        ]
                        if thought_lines:
                            st.markdown(f"💭 **Thought:** {thought_lines[-1].replace('Thought:', '').strip()}")
                        if "observation" in step:
                            st.markdown(f"👁️ **Observation:** {step['observation'][:200]}...")
                    st.divider()

# ── Input ─────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        label="user_input",
        placeholder="Ask me anything — research papers, calculations, web search...",
        label_visibility="collapsed",
        key="input_box"
    )
with col2:
    send = st.button("Send →")

# ── Handle send ───────────────────────────────────────────────────────────────
if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.spinner("Thinking..."):
        response, steps = run_agent(st.session_state.agent, user_input)

    st.session_state.messages.append({
        "role": "agent",
        "content": response,
        "steps": steps
    })
    st.rerun()

# ── Clear ─────────────────────────────────────────────────────────────────────
if st.session_state.messages:
    if st.button("Clear conversation"):
        st.session_state.messages = []
        st.session_state.agent = create_agent()
        st.rerun()