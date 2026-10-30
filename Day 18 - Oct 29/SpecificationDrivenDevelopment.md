# Specification Driven Development(SDD)
SDD is a development paradigm where a detailed specification of the implementation is authored and agreed upon before development begins. Hence, it serves as a single source of truth for what exactly to build and how to build it.

The core of SDD is strictly separating the design and implementation phases, enforcing a "design-first" approach. 

### Design Phase:
In this phase, architects focus entirely on what the system should look like and how should it work, without writing any single code. The goal is to define all the api endpoints, data models, interfaces, acceptance criteria,error handling The benefit is that since there is no code implementation stakeholders can review and update the design very easily without changing any backend logic.

### Why the specification becomes the single source of truth for AI-assisted engineering?
AI generates vulnerable codes which doesn't follow architectural patterns and introducing security failures. The specification acts as active validation gates against these failures. Also the specification acts as a binding contract that automatically dictate how the code behaves. The specification also acts as the central arbiter because every part of the code relies on the same document for e.g:
 - Backend uses the specification to generate the server routing and data verification.
 - Frontend uses the specification to generate API clients and mock servers so that they can build the UI before even the backend is ready.
 - QA team uses the specification to automatically generate test suites and validate that API matches the design.

### Implementation Phase:
The implementation phase starts once the specification document is finished and approved. Developers use automated tools to write the code. Since the specification defines exactly how the system should interact, different teams can start the implementation parallely.
