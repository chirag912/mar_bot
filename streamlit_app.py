import streamlit as st
import openai

# Initialize OpenAI client
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Set the app title
st.title("Elephant Expert Bot")

# Initialize chat history in session state if not present
if "messages" not in st.session_state:
    st.session_state.messages = []

# Function to get response from OpenAI
def get_response(conversation_history, user_input):
    # Define system message for context setting
    system_message = {
        "role": "system",
        "content": "You are an expert on elephants. You can only talk about elephants. \
        If the user asks about anything else, politely steer the conversation back to elephants."
    }

    # Check if the user input is off-topic
    if "elephant" not in user_input.lower():
        return "I can only discuss elephants. Please ask me something about elephants!"

    # Include the system message at the beginning
    messages = [system_message] + conversation_history + [{"role": "user", "content": user_input}]
    
    # Get response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    return response["choices"][0]["message"]["content"]

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  
        st.markdown(message["content"])  

# User input
user_input = st.chat_input("Type your message about elephants...")
if user_input:
    # Append user's message to session state
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Get assistant's response
    assistant_response = get_response(st.session_state.messages, user_input)

    # Append assistant's response to session state
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
