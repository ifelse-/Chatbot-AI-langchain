# Import necessary functions and libraries
from backend.core import run_llm  # Import the function to run an LLM model
import streamlit as st  # Import Streamlit, a web app framework
from streamlit_chat import message  # Import the function to display chat messages
from typing import Set  # Import the typing module to specify data types

# Create a Streamlit app with a header
st.header("Bot Assistant")


if st.button('Check availability'):
    print("click")

if st.button('Check'):
    print("click")

if st.button('Check4'):
    print("click")


# Add custom CSS to position the text_input at the bottom
st.markdown("""
<style>
.stTextInput {
position: fixed;
bottom: 100px;
}

.stSpinner {
position: fixed;
bottom: 50px;
}
</style>
""", unsafe_allow_html=True)

# Get user input as a prompt for the chatbot
prompt = st.text_input("Prompt", placeholder="Enter your prompt here...")

# Initialize session state to store user's prompt history and chat results
if "user_prompt_history" not in st.session_state:
    st.session_state["user_prompt_history"] = []
if "chat_results_history" not in st.session_state:
    st.session_state["chat_results_history"] = []


# Define a function to create a formatted string from a set of source URLs
def create_sources_string(sources_urls: Set[str]) -> str:
    if not sources_urls:
        return ""
    sources_list = list(sources_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"{i+1}, {source}\n"
    return sources_string


# Process user input and generate a chatbot response
if prompt:
    with st.spinner("Generating response..."):
        generated_response = run_llm(query=prompt)  # Generate a response using LLM
        sources = set(
            [doc.metadata["source"] for doc in generated_response["source_documents"]]
        )  # Extract sources from the response documents
        formatted_response = (
            f"{generated_response['answer']} \n\n {create_sources_string(sources)}"
        )  # Create a formatted response string

        # Store user's prompt and chatbot's response in the session state
        st.session_state["user_prompt_history"].append(prompt)
        st.session_state["chat_results_history"].append(formatted_response)

# Display the chat history if there are chatbot responses
if st.session_state["chat_results_history"]:
    for generated_response, user_query in zip(st.session_state["chat_results_history"], st.session_state["user_prompt_history"]):
        message(user_query, is_user=True)  # Display user's query
        message(generated_response)  # Display chatbot's response
