# Tools and Technology for composing agents

## OpenAI SDK
The OpenAI Agents SDK enables you to build agentic AI apps in a lightweight, easy-to-use package with very few abstractions. It's a production-ready upgrade of our previous experimentation for agents, Swarm. The Agents SDK has a very small set of primitives:

- Agents, which are LLMs equipped with instructions and tools
- Agents as tools / Handoffs, which allow agents to delegate to other agents for specific tasks
- Guardrails, which enable validation of agent inputs and outputs

uv add openai-sdk

## Langchain
Langchain is a popular open-source framework for building applications with LLMs. It provides a wide range of tools and abstractions for working with LLMs, including support for agents, chains, and memory. Langchain provides flexibility for multiple LLM providers, comlex chains, RAG building and fine grained control over your pipeline. It is also open source and has a large community of contributors. Langgchain is greae for linear pipelies

uv add langchain, langchain-openai

## Langgraph 
Langgraph is a framework for building agentic applications with LLMs. It provides a graph-based approach to building agents, where agents are represented as nodes in a graph and the edges represent the flow of information between agents. Langgraph provides a visual interface for designing and debugging agentic applications, making it easier to understand and manage complex agent interactions.
Use it for complex flows where you need looping, branching and making decisions about what to do next. 

uv add langgraph

## Crew AI 
Crew AI is a framework for building agentic applications with LLMs. It provides a simple and intuitive interface for building agents, with a focus on ease of use and rapid development. Crew AI provides a set of pre-built agents and tools that can be easily customized and extended to fit specific use cases. It is great for quickly prototyping and building simple agentic applications. Great for multi-agent pipelines where agents have clear roles and responsibilities.

uv add crewai[tools] (create a project first crewai create crew <your_project_name>)

## AutoGen
AutoGen is a framework for building agentic applications with LLMs. It provides a simple and intuitive interface for building agents, with a focus on ease of use and rapid development. AutoGen provides a set of pre-built agents and tools that can be easily customized and extended to fit specific use cases. It is great for quickly prototyping and building simple agentic applications. Great for multi-agent pipelines where agents have clear roles and responsibilities.

uv add autogen 

---

## Comparative Analysis

### OpenAI Agents SDK
|   |
|---|---|
| **When to use** | You are building production agent apps and are happy to be tied to OpenAI models |
| **Learning curve** | **Low** — minimal abstractions, only a handful of primitives to learn |
| **Advantages** | Simple and production-ready; official OpenAI support; built-in guardrails, handoffs, and tracing |
| **Disadvantages** | OpenAI models only; limited to its own primitives; less flexible for non-agent use cases |
| **Best for** | Lightweight, production-grade agents using OpenAI |

---

### Langchain
|   |
|---|---|
| **When to use** | You need multi-provider support, RAG pipelines, or fine-grained control over your LLM pipeline |
| **Learning curve** | **High** — large API surface with many concepts: chains, retrievers, memory, callbacks, etc. |
| **Advantages** | Model-agnostic; huge ecosystem; integrations for virtually every tool and provider; strong open-source community |
| **Disadvantages** | Verbose and complex; abstractions can be confusing; API changes frequently |
| **Best for** | RAG apps, data pipelines, and scenarios requiring multi-provider flexibility |

---

### LangGraph
|   |
|---|---|
| **When to use** | Your agent needs loops, branching, retry logic, or human-in-the-loop interactions |
| **Learning curve** | **High** — requires understanding graphs, typed state management, and conditional routing |
| **Advantages** | Full control over flow; supports cycles and loops; persistent state via checkpointers; visual graph debugging |
| **Disadvantages** | Steep learning curve; lots of boilerplate; overkill for simple linear pipelines |
| **Best for** | Complex stateful agents needing retry loops, evaluation steps, or mid-flow user interaction |

---

### Crew AI
|   |
|---|---|
| **When to use** | You have a clear team of specialist agents each with a distinct role and task |
| **Learning curve** | **Low–Medium** — YAML-driven config and CLI scaffolding hide most complexity |
| **Advantages** | Rapid scaffolding; role-based agent design; built-in short/long-term and entity memory; sequential and hierarchical processes |
| **Disadvantages** | Opinionated structure; hard to customise flow beyond sequential/hierarchical; separate project scaffold per crew |
| **Best for** | Multi-agent pipelines with clear division of labour (e.g. researcher → analyst → writer) |

---

### AutoGen
|   |
|---|---|
| **When to use** | You need agents to collaborate conversationally, iterating and critiquing each other's work |
| **Learning curve** | **Medium** — intuitive agent/team model, but async patterns add complexity |
| **Advantages** | Flexible conversation patterns; supports round-robin and group chat; good for iterative refinement workflows |
| **Disadvantages** | Less mature ecosystem; fewer integrations than Langchain; multi-agent conversations can be harder to debug |
| **Best for** | Iterative multi-agent collaboration and conversational task solving |