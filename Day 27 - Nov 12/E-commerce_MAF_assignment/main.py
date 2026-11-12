import json
from dotenv import load_dotenv
from pathlib import Path
from typing import Never
import asyncio
import os
from dataclasses import dataclass

from agent_framework.openai import OpenAIChatClient
from agent_framework import (Agent,WorkflowBuilder,
                             WorkflowContext,executor,
                             Executor,handler,response_handler)
from openai import AsyncOpenAI

PROJECT_ROOT = Path(__file__).resolve().parent
load_dotenv(str(PROJECT_ROOT / ".env"))


@dataclass
class HumanApprovalRequest:
    return_item:dict
    prompt: str

# =====================================================
# HUMAN-IN-THE-LOOP APPROVAL GATEWAY(Before doing this
# check if the workflow is running properly)
# =====================================================
class ApprovalGateway(Executor):
    def __init__(self):
        super().__init__(id="approval_gateway")

    @handler
    async def review(self,
                     return_item: dict,
                     ctx: WorkflowContext[dict]) -> None:
        needs_approval =(
            return_item["amount_inr"] >= 25000 or
            return_item["days_since_delivery"] > 30 or
            return_item["invoice_available"] == False or
            return_item["item_condition"] == "USED" or
            (return_item["item_condition"] == "DAMAGED" and return_item["photo_evidence_available"] == False) or
            return_item["previous_returns_90_days"] >= 3 or
            return_item["risk"] == "HIGH"
        )

        if not needs_approval:
            return_item["decision"] = "AUTO_APPROVED"
            return_item["decision_by"] = "Demo approval policy"

            print("ApprovalGateway: automatic approval")
            await ctx.send_message(return_item)
            return

        # PAUSING the workflow, wait for human approval
        print("ApprovalGateway: PAUSED - awaiting human")
        await ctx.request_info(
            request_data = HumanApprovalRequest(
                return_item = return_item,
                prompt = (
                    f"Review {return_item['request_id']} | "
                    f"{return_item['product']} | "
                    f"INR {return_item['amount_inr']:,} | "
                    f"Risk: {return_item['risk']}"
                ),
            ),
            response_type=str,
        )

    @response_handler
    async def on_human_decision(self,
                original_request : HumanApprovalRequest,
                response : str,
                ctx: WorkflowContext[dict]) -> None:
        return_item = dict(original_request.return_item)
        decision = response.strip().lower()

        if decision not in {"approve", "reject"}:
            decision="reject"

        return_item["decision"] = (
            "HUMAN APPROVED"
            if decision == "approve"
            else "HUMAN REJECTED"
        )

        return_item["decision_by"] = "Human Manager"

        # RESUME workflow
        await ctx.send_message(return_item)



# ==============================================
# Creating agents and workflow
# ==============================================

def build_workflow(chat_client : OpenAIChatClient):
    # Agent 1 - Eligibility Agent
    eligibility_agent = Agent(
        client = chat_client,
        name="EligibilityAgent",
        instructions = (
            "You review each return request against the company's return policy. Identify whether the request meets "
            "eligibility requirements and explain any exceptions. Don't invent any new "
            "return policy. Respond within 2 sentences."
        ),
    )

    # Agent 2 - Risk Agent
    risk_agent = Agent(
        client = chat_client,
        name="RiskAgent",
        instructions = (
            "Analyze potential risks such as unusual return frequency, missing evidence, or high-value requests. "
            "Use only the supplied data. "
            "Mark HIGH when item_condition is DAMAGED, "
            "or when invoice_available is false "
            "or when the return_reason is justified. "
            "Otherwise mark LOW. "
            "Reply with one word only: HIGH or LOW."
        ),
    )

    # Agent 3 - Customer Response Agent
    customer_response_agent = Agent(
        client = chat_client,
        name="CustomerResponseAgent",
        instructions = (
            "Generate a customer-facing message based on the final workflow decision. The message must "
            "accurately communicate approval or rejection without claiming that a refund or replacement has "
            "already been completed."
        ),
    )
    # ==============================================
    # Executor 1 - Returns Review
    # ==============================================

    @executor(id="returns_review")
    async def returns_review(
            return_item: dict,
            ctx: WorkflowContext[dict]
    )-> None:
        print(" Eligibility Agent is checking justification ")
        result = await eligibility_agent.run(
            json.dumps(return_item)
        )

        await ctx.send_message({
            **return_item,
            "review" : result.text.strip(),
        })

    # ==============================================
    # Executor 2 - Risk Review
    # ==============================================
    @executor(id="risk_review")
    async def risk_review(
            return_item : dict,
            ctx: WorkflowContext[dict]
    )-> None:
        print(" Risk Agent is assessing return ")

        result = await risk_agent.run(
            json.dumps(return_item)
        )

        risk = result.text.strip().upper().strip(". ")
        if risk not in ["HIGH", "LOW"]:
            risk = "HIGH"

        await ctx.send_message({
            **return_item,
            "risk" : risk,
        })

    # ==============================================
    # Executor 3 - Customer Response
    # ==============================================
    @executor(id="customer_response")
    async def customer_response(
            return_item:dict,
            ctx: WorkflowContext[Never,str]
    )->None:
        print(" CustomerResponse Agent: preparing final response")
        result = await customer_response_agent.run(
            json.dumps(return_item)
        )

        await ctx.yield_output(
            f"{return_item['request_id']} -> "
            # f"{return_item['decision']} \n"
            f"{result.text.strip()}"
        )

    # -------------------------------------------------
    # CREATE GRAPH
    # -------------------------------------------------
    approval_gateway = ApprovalGateway()  # Added during Human in the loop process
    return (
        WorkflowBuilder(
            start_executor = returns_review
        )
        .add_edge(returns_review,risk_review)
        .add_edge(risk_review,approval_gateway)  #written after adding human in the loop
        .add_edge(approval_gateway,customer_response)
        .build()
    )

# =====================================================
# EXECUTE WORKFLOW WITH HUMAN APPROVAL
# =====================================================
async def run_one(workflow, return_item : dict) -> None:
    responses = None # Stores the human responses
    first_run = True # Starting the workflow for first
    # time? Or resuming it after human input?
    while True:
        # Initial or resumed execution
        if first_run:
            stream = workflow.run(
                return_item,
                stream = True,
            )
            first_run=False
        else:
            stream = workflow.run(
                stream=True,
                responses=responses,
            )
        pending = {}
        completed = False

        async for event in stream:
            if event.type == "request_info": # ctx.request_info sets this event_type
                pending[event.request_id] = event.data
            elif event.type == "output":
                print("\n FINAL RECORD \n" + str(event.data))
                completed = True

        if completed:
            return
        if not pending:
            raise RuntimeError(
                "Workflow stopped without output "
                "or approval request"
            )

        responses = {}

        for request_id,request in pending.items():
            print("\n" + "=" * 50)
            print("MANAGER APPROVAL REQUIRED")
            print(request.prompt)

            print(
                "Returns review:",
                request.return_item["review"],
            )

            while True:

                answer = input(
                    "Type approve or reject: "
                ).strip().lower()

                if answer in {"approve", "reject"}:
                    break

                print("Please type approve or reject.")

            responses[request_id] = answer


# =====================================================
# MAIN APPLICATION
# =====================================================
async def main()->None:
    print("="*60)
    print("MICROSOFT AGENT FRAMEWORK")
    print("RETURNS AND REFUNDS SYSTEM")
    print("Authentication: Azure Foundry API Key")

    # Load the credentials
    api_key= os.getenv("AZURE_OPENAI_API_KEY")
    base_url = os.getenv("AZURE_OPENAI_BASE_URL")
    deployment = os.getenv("AZURE_OPENAI_MODEL")
    print("\nAzure Foundry configuration loaded.")
    print(f"Endpoint: {base_url}")
    print(f"Deployment: {deployment}")

    # -------------------------------------------------
    # LOAD RETURNS DATA
    # -------------------------------------------------
    returns_file = (PROJECT_ROOT / "returns.json")

    with returns_file.open(encoding="utf-8") as file:
        returns = json.load(file)

    print(f"\n Total no of returns filed: {len(returns)}")

    # -------------------------------------------------
    # CONNECT TO AZURE FOUNDRY
    # -------------------------------------------------
    async with AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
    ) as sdk_client:
        chat_client = OpenAIChatClient(
            model=deployment,async_client=sdk_client)

        print("Azure Foundry client initialized")

        # ---------------------------------------------
        # BUILD WORKFLOW for non human in the loop
        # ---------------------------------------------

####### Uncommnet the following two lines if you dont' want to
####### build human in the loop

        # workflow = build_workflow(chat_client)
        # print("Graph workflow built.")

        # ---------------------------------------------
        # PROCESS RETURNS
        # ---------------------------------------------

        for return_item in returns:
            print("\n"+"="*60)
            print(f"Processing Request: {return_item['request_id']}")
            print(f"Return Reason: {return_item['return_reason']}")
            print("="*60)

            workflow = build_workflow(chat_client)
            await run_one(workflow, return_item)

######### Uncomment the following lines and comment
######### the above two lines if you don't want
######### human in the loop

            # Run the workflow
            # result = await workflow.run(return_item)

        #     # Display outputs
        #     for op in result.get_outputs():
        #         print("\n"+"-"*60)
        #         print("FINAL RESPONSE")
        #         print('-'*60)
        #         print(op)
        #         print('-'*60)
        # print("\n"+"="*60)
        # print("ALL RETURNS PROCESSED")
        # print("="*60)


if __name__ == "__main__":
    asyncio.run(main())





