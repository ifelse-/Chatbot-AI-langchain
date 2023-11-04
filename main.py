from backend.core import run_llm
import streamlit as st
from streamlit_chat import message
from typing import Set

st.header("Bot Assistant")

prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")

if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []

if "chat_results_history" not in st.session_state:
    st.session_state["chat_results_history"] = []


def create_sources_string(sources_urls: Set[str]) -> str:
    if not sources_urls:
        return ""
    sources_list = list(sources_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}, {source}\n"
    return sources_string


if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(query=prompt)
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )
        formatted_response = (
            f"{generated_response['result']}"
        )

        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_results_history"].append(formatted_response)

if st.session_state["chat_results_history"]:
    for generated_response, user_query in zip(
            st.session_state["chat_results_history"],
            st.session_state["user_prompt_history"],
    ):
        message(user_query, is_user=True)
        message(generated_response)
