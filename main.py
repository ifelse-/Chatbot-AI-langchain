# Import necessary functions and libraries
from backend.core import run_llm  # Import the function to run an LLM model
import streamlit as st  # Import Streamlit, a web app framework
from streamlit_chat import message  # Import the function to display chat messages
from typing import Set  # Import the typing module to specify data types

st.markdown("""
<style>
.bg-header {
    font-size: 20px !important;
    font-weight: bold  !important;
}

.block-container {
    padding: 2rem 1rem 10rem !important;
}
</style>
""", unsafe_allow_html=True)

# Create a Streamlit app with a header
st.header("Personal Bot Assistant")
st.text("By Marvin Elmore. \nBelow is an example of a user name John Smith that has vector data in Pinecone. \nThis is a Streamlit UX")

st.markdown("John Smith, a resilient Ohio resident, faced financial challenges while dedicating long hours to a local warehouse. Battling living costs and unexpected medical bills, he reached a crossroads. Fueled by determination, John transformed his life, opening a candle business with a $2,000 investment. Residing in New York, he navigates hardships, committed to a brighter future. In his personal life, John shares a bond with Max, his loyal Golden Retriever, finding solace in Ohio walks. Beyond financial stability, he dreams of creating a community space through his business, driven by a frugal lifestyle. Seeking companionship, John believes love adds depth to life.")
# st.text("Savings Account Balance: $3,000  | Monthly Income: $2,500  \nFixed Expenses: | Rent/Mortgage: $1,000  \nUtilities (Electricity, Water, Gas, Internet, etc.): $200 \nCar Loan/Insurance: $300 | Groceries/Food: $250 \nTransportation (Gas, Public Transport, etc.): $100 \nVariable Expenses: | Dining Out/Entertainment: $150 \nTravel/Vacation: $100")

st.markdown('<p class="bg-header">Prompts (E.g.)</p>', unsafe_allow_html=True)
st.text("Personal Growth: Inquire about John's personal growth")
st.text("Financial Insights: What are John's fixed expenses?")
st.text("Expense Question: What is my Balance this month and can you break it down for me?")

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
prompt = st.text_input("Enter Prompt", placeholder="Enter your prompt here...")

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
    # for i, source in enumerate(sources_list):
    #     sources_string += f"{i+1}, {source}\n"
    # return sources_string


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
