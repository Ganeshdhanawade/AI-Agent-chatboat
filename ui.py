import streamlit as st
import requests

# streamlit app configuration
st.set_page_config(page_title="LangGraph.Agent.UI",layout="centered")

# Define API endpoint
API_URL = "http://127.0.0.1:8000/chat"

#predefined list of supported model name
MODEL_NAMES = [
    "llama3-70b-8192", #model1: llama 3 with specific cofiguration
    "mixtral-8x7b-32768" #mistral with specific configuration
]

#streamlit UI Elements
st.title("LangGraph Chatbot Agent")
st.write("Interact with the LangGraph-based agent using this interface.")

#input box for system prompt
given_system_prompt = st.text_area("Define you AI agent:", height=10, placeholder="Type your system prompt here...")

#dropdown for selecting the model
selected_model = st.selectbox("Select Model:", MODEL_NAMES)

#input box for you messages
user_input = st.text_area("Enter your messages", height=150, placeholder="Type your massage here...")

#Button to send the query
if st.button("Send Query"):
    if user_input.strip():
        try:
            #send the input the FastAPI backend
            payload = {"messages": [user_input],"model_name":selected_model,"system_prompt":given_system_prompt}
            response = requests.post(API_URL, json=payload)

            #display the responce
            if response.status_code == 200:
                response_data = response.json()
                if "error" in response_data:
                    st.error(response_data['error'])
                else:
                    ai_response = [
                        message.get("content", "")
                        for message in response_data.get("messages",[])
                        if message.get("type") == "ai"
                    ]
                    
                    if ai_response:
                        st.subheader("Agent Response:")
                        st.markdown(f"**final.Response:** {ai_response[-1]}")
                    else:
                        st.warning("No AI response found in the agent output.")

            else:
                st.error(f"request fail with the status code {response.status_code}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("please inter the massage before clicking 'send quary'.")