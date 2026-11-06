from dotenv import load_dotenv
import os
from pathlib import Path
from langchain.agents import create_agent
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

from tools import calculate_dining_cost,search_particular_restaurant
from guardrails import contains_pii,clean_output

PROJECT_ROOT = Path(__file__).resolve().parent

# 1. Load environment
load_dotenv(PROJECT_ROOT / ".env")

# 2. Create model
if not os.getenv("KEY"):
    raise SystemExit("Please set the environment variable `KEY`")

api_key = os.getenv("KEY")
model_name = os.getenv("MODEL")

model = ChatOpenRouter(
    model=model_name,
    api_key=api_key,
    temperature=0,
)

# 3. Create Agent
agent = create_agent(
    model=model,
    tools=[search_particular_restaurant,calculate_dining_cost],
    system_prompt = (
        "You are helpful Restaurant Reservation AI Assistant."
        "Only answer questions about restaurants, available seats and cost."
        "Use the tools for fetching the restaurant details and calculating costs."
        "Never invent any Restaurant names or prices."
    ),
    checkpointer = InMemorySaver(),
)

# 4. Run app and test
if __name__ == "__main__":
    thread_number = 1  # This is like a unique id for each conversation
    previous_count = 0
    print("LANGCHAIN Restaurant Reservation AI Assistant")
    print("\n Type exit to quit")
    while True:
        question = input("\nYou> ").strip()
        if question.lower() in ["exit", "quit"]:
            break
        if question.lower() == "/new":
            thread_number += 1
            previous_count = 0
            print("New Conversation start...")
            continue
        if not question:
            continue
        if contains_pii(question):
            print("PII detected. Please remove personal contact details")
            break
        config = {
            "configurable" : {
                "thread_id" : f"workshop - {thread_number}",
            }
        }
        try:
            result = agent.invoke(
                {
                    "messages":[
                        {"role" : "user","content" : question}
                    ]
                },
                config = config
            )
            messages = result["messages"]
            new_messages = messages[previous_count:]
            previous_count = len(messages)

            for message in new_messages:
                if isinstance(message,AIMessage):
                    for call in message.tool_calls:
                        print("[TOOL]: ",call["name"])
                        print("Arguments: ",call["args"])

                if isinstance(message,ToolMessage):
                    print("[TOOL RESULT]: ",message.content)
            print("\n Agent Response: ", clean_output(messages[-1].content))
        except Exception as e:
            print("Error: ",e)