# What is AutoGen Core?
AutoGen Core is a framework for building AI agents that can autonomously perform complex tasks by leveraging multiple tools and resources. It provides a structured way to define agents, their capabilities, and the tools they can use to achieve their goals. AutoGen Core allows developers to create agents that can interact with various APIs, perform web searches, manage files, and more, all while maintaining a clear separation of concerns between the agent's logic and the tools it utilizes. (it is like a runtime)

# What is AutoGenChat? 
AutoGenChat is a specific implementation of an AI agent built using the AutoGen Core framework. It is designed to facilitate natural language interactions between users and the agent, allowing users to communicate with the agent in a conversational manner. AutoGenChat can be used for a variety of applications, such as customer support, virtual assistants, or any scenario where a conversational interface is beneficial. It leverages the capabilities of AutoGen Core to provide a seamless and interactive experience for users while performing tasks and accessing tools as needed.

# Core Concepts 
## Models
In AutoGen, models refer to the underlying AI models that power the agent's capabilities. These models can include language models, vision models, or any other type of model that enables the agent to understand and generate content. The choice of models can significantly impact the agent's performance and the range of tasks it can handle.

## Messages
Messages are the primary means of communication between the user and the agent in AutoGenChat. They can be in the form of text, images, or other media types, depending on the capabilities of the agent. Messages allow users to interact with the agent, ask questions, provide instructions, or request information. The agent processes these messages and generates appropriate responses based on its understanding and the tools it has access to.

## Agents
Agents in AutoGen are autonomous entities that can perform tasks, make decisions, and interact with users. They are defined by their capabilities, the tools they can use, and the logic that governs their behavior. Agents can be designed to handle specific tasks or be more general-purpose, depending on the use case. They can also be configured to use different models and tools to achieve their goals effectively.

# Teams
Teams in AutoGen refer to groups of agents that can collaborate to achieve a common goal. Each agent within a team can have its own set of capabilities and tools, and they can communicate with each other to coordinate their actions. Teams allow for more complex and sophisticated interactions, as multiple agents can work together to solve problems, share information, and provide a richer user experience.