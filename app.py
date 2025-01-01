#importing the necessary setup FastAPI, LangGraph and LangChain
from fastapi import FastAPI #FastAPI framework for creating the web application
from pydantic import BaseModel # use for structure data and models
from typing import List #it can hit for type annotation
from langchain_community.tools.tavily_search import TavilySearchResults # handle search of agent
import os
from langgraph.prebuilt import create_react_agent #function to create react agent
from langchain_groq import ChatGroq #use for interact with llm
from dotenv import load_dotenv
import uvicorn
load_dotenv()

#retrive the api 
os.environ["TAVILY_API_KEY"]= os.getenv('tavity_api_key')

#predefined list of supported model name
MODEL_NAMES = [
    "llama3-70b-8192", #model1: llama 3 with specific cofiguration
    "mixtral-8x7b-32768" #mistral with specific configuration
]

#initialize the tavity search to specified maximum number of results.
tool_tavity = TavilySearchResults(max_results=2) #allow to retrive upto 2 results

##add tavity to the tools
tools = [tool_tavity,]

#FastAPI application setup with a title
app = FastAPI(title="LangGraph AI Agent")

#define the request schema using Pydantic's BaseModel
class RequestState(BaseModel):
    model_name : str   # Name of the model to use for processing the request
    system_prompt : str # system prompt for initialization the model
    messages : List[str] # List of models in the chat

# Define an endpoint for handling chat requests
@app.post("/chat")
def chat_endpoint(request: RequestState):
    """
    API endpoint to interact with the chatbot using LangGraph and tools.
    Dynamically selects the model secified in the request.
    """
    if request.model_name not in MODEL_NAMES:
        return {"error": "Invalid model name. Please select a valid model."}
    
    #initialize the LLM with selected model
    llm = ChatGroq(groq_api_key = os.getenv("groq_api_key"),model=request.model_name)

    #create a ReAct agent using the selected LLM and tools
    agent = create_react_agent(llm, tools=tools, state_modifier=request.system_prompt)

    # create the initial state of the processing
    state = {"messages":request.messages}

    #process the state using the agent
    result = agent.invoke(state)  #this is the result of the model

    #return the result
    return result

#Run the application if executed as main script
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1',port=8000) #run fastapi in the uvicorn