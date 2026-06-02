import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph, END
from langchain_groq import ChatGroq

# GROQ MODEL
llm = ChatGroq(
    groq_api_key="",
    model_name="llama-3.1-8b-instant"
)

# STATE
class State(TypedDict):
    message: str

# CHATBOT NODE
def chatbot(state):
    reply = llm.invoke(state["message"])
    return {"message": reply.content}

# LANGGRAPH
graph = StateGraph(State)

graph.add_node("chatbot", chatbot)

graph.set_entry_point("chatbot")

graph.add_edge("chatbot", END)

app = graph.compile()

# STREAMLIT UI
st.title("🤖 Simple LangGraph Chatbot")

user = st.text_input("You:")

if st.button("Send"):

    result = app.invoke({
        "message": user
    })

    st.success(result["message"])
