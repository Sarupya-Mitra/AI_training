# Microsoft Agent Framework (MAF)
MAF is a toolkit for building agents and multi-agent workflows in Python and .NET.

It provides developers with a structured way to create AI agents that can:
- Understand user instuctions and respond intelligently.
- Use tools, APIs and external services.
- Maintain conversation context and state.
- Execute multi-step workflows
- Coolaborate with other AI agents and coordinate complex businees processes.
- Integrate with enterprise applications and cloud services.

MAF is intended to support the development of agentic applications, where AI agents can reason, use tools, make decisions and execute tasks through structured workflows.

## Important concepts of MAF
### Agents
An agent is an AI-powered software component that can understand instruction, interacts with an LLM, use tools and perform tasks.
For example: in an employee-supoort application, there can be:
- HR Agent - answering employee policy questions.
- IT support Agent - handling technical support requests.
- Finance Agent - answering expense-related questions.

Each agent can have its own:
- Name,
- System Prompt
- LLM configuration,
- Tools and functions,
- Conversation state
- Responsibilities

### Tools and Function calling
Tools allow agents to interact with external systems and perform actual operations.
For example, an HR agent might need to:
- Retrieve employee information
- Check leave balance
- Fetch company policies

So instead of simply generating an answer, the agent can invoke registered function to obtain information or perform an operation.

### Multi-Agent Orchestration
MAF allows multiple specialized agents to collaborate on larger task, so instead of having one agent perform everything, responsibilities are distributed among specialized agents.
MAF supports different orchestration patterns:
- Sequential - Agents execute one after another
- Concurrent - Multiple agents execute tasks simultaneously
- Handoff - One agent transfers control to another
- Group Collaboration - Multiple agents collaborate to solve a problem.

### Workflows
A workflow is a structured way of defining how tasks should execute.

For example, considering a loan approval application, a possible workflow can be:
1) Receive loan application.
2) Verify customer details.
3) Check credit information.
4) Calculate eligibility.
5) Request human approval.
6) Generate final decision. 
