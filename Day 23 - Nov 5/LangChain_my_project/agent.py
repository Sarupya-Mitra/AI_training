
import os
from dotenv import load_dotenv

from langchain.agents import create_agent
# from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import InMemorySaver

from tools import search_workshops, calculate_workshop_fee,match_coupon_codes,find_cheapest_workshop
from guardrails import contains_pii,clean_output


# STEP 1: Load environment
load_dotenv()

# STEP 2: Create model
# model = ChatOpenAI(
#     model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
#     temperature=0
# )
api_key = os.getenv("KEY")
model_name = os.getenv("MODEL")

model = ChatOpenRouter(
    model=model_name,
    api_key=api_key,
    temperature=0,
)

# STEP 3: Create agent
agent = create_agent(
    model=model,
    tools=[search_workshops, calculate_workshop_fee,find_cheapest_workshop,match_coupon_codes],
    # system_prompt="You are a helpful workshop assistant.",
    # The above system prompt is very basic, no guardrail is provided.
    system_prompt=(
        "You are a Workshop AI Assistant. "
        "Only answer questions about available workshops, "
        "training details and fees. "
        "Use the tools for workshop information and calculations. "
        "Never invent workshop names or prices. "
        "For unrelated questions, say: "
        "'I can only help with workshops and their fees.' "
        "If the user says yes after viewing a workshop, "
        "ask how many participants will attend. "
        "Remember the selected workshop when calculating fees."
        "Also before calculating fees ask whether user has any coupon codes."
        "COUPON VALIDATION RULES:"
        "1. If the user provides a coupon code, extract only"
           "the coupon code from their message."
        "2. Call match_coupon_codes with the extracted code."
        "3. Never assume a coupon code is valid without calling"
           " the tool."
        "4. Never invent coupon codes or discounts."
        "5. If the tool returns a valid coupon, retrieve its"
          " discount percentage."
        "6. Apply the discount to the total workshop fee."
        "7. If the tool returns 'Coupon code not found',"
          " inform the user that the coupon is invalid."
        "8. If the user does not have a coupon, calculate"
          " the original fee without a discount. "
    ),
    checkpointer=InMemorySaver()
)
# Agent Creation is complete

# STEP 4: Run application and test it
if __name__ == "__main__":

    thread_number = 1
    previous_count = 0

    print("LangChain Workshop AI Agent")
    print("Type /new for a new conversation")
    print("Type exit to quit")

    while True:
        question = input("\nYou: ").strip()

        if contains_pii(question):
            print("PII detected. Please remove personal contact details.")
            break

        if question.lower() == "exit":
            break

        if question.lower() == "/new":
            thread_number += 1
            previous_count = 0
            print("New conversation started.")
            continue

        if not question:
            continue

        config = {
            "configurable": {
                "thread_id": f"workshop-{thread_number}"
            }
        }

        try:
            result = agent.invoke(
                {
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                },
                config=config
            )

            messages = result["messages"]
            new_messages = messages[previous_count:]
            previous_count = len(messages)

            for message in new_messages:

                if isinstance(message, AIMessage):
                    for call in message.tool_calls:
                        print("[TOOL]:", call["name"])
                        print("Arguments:", call["args"])

                if isinstance(message, ToolMessage):
                    print("[TOOL RESULT]:", message.content)

            print("\nAgent:", clean_output(messages[-1].content))

        except Exception as error:
            print("Error:", error)
