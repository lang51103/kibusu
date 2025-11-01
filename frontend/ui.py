import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import asyncio
import nest_asyncio
from langchain_core.messages import HumanMessage, AIMessageChunk
from langgraph.types import Command
from src.nova.graph import build_graph, AgentState


nest_asyncio.apply()
st.set_page_config(page_title="Ralph Assistant", page_icon="🤖", layout="centered")
st.title("🤖 Ralph - AI Assistant")

# initialize session
if "graph" not in st.session_state:
    st.session_state.graph = asyncio.run(build_graph())
if "config" not in st.session_state:
    st.session_state.config = {"configurable": {"thread_id": "1"}}
if "messages" not in st.session_state:
    st.session_state.messages = []
if "interrupt" not in st.session_state:
    st.session_state.interrupt = None
if "yolo_mode" not in st.session_state:
    st.session_state.yolo_mode = False

graph = st.session_state.graph
config = st.session_state.config

# render messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# handle interrupt UI
if st.session_state.interrupt:
    interrupt_value = st.session_state.interrupt
    st.warning("⚠️ Human Approval Required")
    st.json(interrupt_value)
    col1, col2, col3 = st.columns(3)
    action = None
    data = None

    if col1.button(" Continue"):
        action = "continue"
    elif col2.button("✏️ Update"):
        action = "update"
        data = st.text_input("Enter update data:")
    elif col3.button("💬 Feedback"):
        action = "feedback"
        data = st.text_input("Enter feedback data:")

    if action:
        async def handle_resume():
            with st.chat_message("assistant"):
                placeholder = st.empty()
                full_reply = ""
                async for msg_chunk, meta in graph.astream(
                    input=Command(resume={"action": action, "data": data}),
                    stream_mode="messages",
                    config=config
                ):
                    if isinstance(msg_chunk, AIMessageChunk):
                        full_reply += msg_chunk.content or ""
                        placeholder.markdown(full_reply)
            st.session_state.messages.append({"role": "assistant", "content": full_reply})
            thread_state = graph.get_state(config=config)
            st.session_state.interrupt = thread_state.interrupts[0].value if thread_state.interrupts else None

        asyncio.run(handle_resume())
        st.rerun()

# handle chat input
if user_input := st.chat_input("Type your message..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    graph_input = AgentState(
        messages=[HumanMessage(content=user_input)],
        yolo_mode=st.session_state.yolo_mode
    )

    async def run_graph():
        with st.chat_message("assistant"):
            placeholder = st.empty()
            full_reply = ""
            async for msg_chunk, meta in graph.astream(
                input=graph_input,
                stream_mode="messages",
                config=config
            ):
                if isinstance(msg_chunk, AIMessageChunk):
                    full_reply += msg_chunk.content or ""
                    placeholder.markdown(full_reply)
            st.session_state.messages.append({"role": "assistant", "content": full_reply})

        # after graph finishes, check for interrupts
        thread_state = graph.get_state(config=config)
        if thread_state.interrupts:
            st.session_state.interrupt = thread_state.interrupts[0].value
        else:
            st.session_state.interrupt = None

    asyncio.run(run_graph())
    st.rerun()
