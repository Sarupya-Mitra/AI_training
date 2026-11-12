### 1) result = await workflow.run(return_item)
In main you wrote this code, to run your workflow. You pass
each return_item in it.

### 2) WorkflowBuilder(start_executor = returns_review)
### .add_edge(returns_review,risk_review)
###        .add_edge(risk_review,customer_response)
###        .build()

This was your workflow definition. It starts or first calls
"returns_review" executor, then returns_review calls "risk_review"
executor and finally "risk_review" calls "customer_response"
executor. 

### 3) async def returns_review(return_item: dict,ctx: WorkflowContext[dict]
Now returns_review expects a dict as an argument. Since you had
already passed return_item in workflow.run(return_item), this
return_item will be passed to returns_review. 
The workflowcontext is automatically created by the framework.

### 4) await ctx.send_message({**return_item,"review" : result.text.strip(),})
workflowcontext enables the communication between different
executors. So send_message will send the message to the next executor.
**return_item means all the fields of the return_item
So we are sending all the fields of the return_item and also an 
additional field review.
So if initially return_item was:
return_item = {
    "request_id": "RET101",
    "item_condition": "DAMAGED",
    "return_reason": "Product arrived damaged",
    "invoice_available": True
} then the output of returns_review will be:
{
    "request_id": "RET101",
    "item_condition": "DAMAGED",
    "return_reason": "Product arrived damaged",
    "invoice_available": True,
    "review": "Eligible for return"
}
This is received by the next executor (risk_review).

### 5) await ctx.send_message({**return_item,"risk" : risk,})
Similarly, risk_review also adds a field "risk" to the json 
it received.
So if it received :
{
    "request_id": "RET101",
    "item_condition": "DAMAGED",
    "return_reason": "Product arrived damaged",
    "invoice_available": True,
    "review": "Eligible for return"
}
the output will be:
{
    "request_id": "RET101",
    "item_condition": "DAMAGED",
    "return_reason": "Product arrived damaged",
    "invoice_available": True,
    "review": "Eligible for return",
    "risk": "HIGH"
}
This is sent to the next executor(customer_response).

### 6) await ctx.yield_output(f"{return_item['request_id']} -> "
### f"{result.text.strip()}")
yield_output() will publish the final output to the 
workflow's external caller. The caller was:
*result = await workflow.run(return_item)*. Hence when
I do 'for op in result.get_outputs(): .. print(op)' ;
the results look like RET210 -> bla bla bla, because I had
written *f"{return_item['request_id']} -> {result.text.strip()}"*
inside the yield_output function.

**Till now we have not introduced the human in the loop**
** Now we will add the human in the loop**

### 7) HumanApprovalRequest

### 8)  await ctx.request_info(request_data = HumanApprovalRequest(
### return_item = return_item,prompt = (...),
### ), response_type=str,)
This pauses the workflow and creates an information request. 
It expects the human response to be a str, hence we have 
written 'response_type=str'.


### 9) @response_handler
###    async def on_human_decision
Once the human responds, this method will be called.

### 10) def run_one
It runs one request through the workflow.
Its responsibilities are:
- Start the workflow.
- Listen for workflow events.
- Detect human approval requests.
- Display the approval request to the manager.
- Collect the manager's decision.
- Send the decision back to the workflow.
- Resume the workflow.
- Display the final output.

### 11) What is stream?
Normally, we execute:
'result = await workflow.run(return_item)'
This waits for the workflow to finish 
and gives you the final result.

But here, stream = workflow.run(return_item,stream=True),
We're asking the workflow to provide events as 
execution progresses.

This is useful for Human-in-the-Loop because you don't 
have to wait until the entire workflow finishes to 
discover that a human's approval is required.

-> Without stream=True, we do ''result = await workflow.run(return_item)'
What happens?
- Returns Review executes.
- Risk Review executes.
- Approval Gateway executes.
- Customer Response executes.
Workflow completes. You receive the final result.
You generally receive the result after the workflow finishes.

-> With stream=True
The workflow still executes:
- Returns Review.
- Risk Review.
- Approval Gateway.
- Customer Response.
But instead of waiting for the entire workflow to finish 
before accessing results, you receive events as they are 
produced.

