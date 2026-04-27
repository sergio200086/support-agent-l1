from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage
from tools.db_tool import get_user_profile
from tools.ticket_creation_tool import create_jira_incident
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
import os

load_dotenv() 
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", api_key=api_key)

diana_prompt = (
    "You are a professional Tier 1 Technical Support Agent for 'Telecom INC'. "
    "Your name is Diana. You must always speak in Spanish (Colombian style). "
    "If the user asks if you are an AI, be honest. "
    "CRITICAL RULE: Before providing any account details or technical status, "
    "you MUST ask for and receive the user's national ID (Cédula/CC). "
    "Once you have the CC, use the 'get_user_profile' tool to help the user."
    "If the user provides an invalid ID format (e.g., letters or symbols), explain politely that the ID must contain only numbers and ask for it again."
)

memory = MemorySaver()
tools = [get_user_profile, create_jira_incident]

agent_executor = create_react_agent(
    llm,
    tools,
    prompt=diana_prompt,
    checkpointer=memory
)


def chat_with_diana():
    config = {"configurable":{"thread_id": "user_session_001"}}
    print("--- Diana de TeleCom INC ha entrado al chat ---")
    while True:
        user_input = input("Usuario: ")
        if user_input.lower() in ["salir", "exit", "quit"]:
            break

        for event in agent_executor.stream(
            {"messages": [("user", user_input)]}, 
            config # type: ignore
        ):
            for node, value in event.items():
                if node == "agent": 
                    last_msg = value["messages"][-1].content
                    if isinstance(last_msg, list):
                        for item in last_msg:
                            if isinstance(item, dict) and item.get("type") == "text":
                                print(f"Diana: {item['text']}")
                    else:
                        print(f"Diana: {last_msg}")

if __name__ == "__main__":
    chat_with_diana()