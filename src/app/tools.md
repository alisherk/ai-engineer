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

## Crew AI 
Crew AI is a framework for building agentic applications with LLMs. It provides a simple and intuitive interface for building agents, with a focus on ease of use and rapid development. Crew AI provides a set of pre-built agents and tools that can be easily customized and extended to fit specific use cases. It is great for quickly prototyping and building simple agentic applications. Great for multi-agent pipelines where agents have clear roles and responsibilities.

uv add crew-ai (create a project first crewai create crew <your_project_name>)