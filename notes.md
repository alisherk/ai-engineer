
# Agentic Workflow Design Patterns

## Overview

This document outlines common design patterns for building agentic AI workflows. These patterns help structure complex LLM-based systems by breaking down tasks, managing execution flow, and ensuring quality outputs. Each pattern addresses specific use cases and can be combined to create sophisticated AI applications.

---

## 1. Prompt Chaining

### Description
The output of one prompt is used as the input for the next prompt, creating a sequential pipeline of LLM interactions. This allows for complex workflows to be built by chaining together multiple prompts.

### Workflow
```
Input -> LLM1 (Output1) -> LLM2 (Output2) -> LLM3 (Final Output)
```

### When to Use
- Multi-step reasoning tasks requiring sequential processing
- Tasks where each step builds upon the previous result
- Document processing pipelines (e.g., extract → summarize → analyze)
- Workflows where intermediate steps need transformation

### Example Use Cases
- Research paper analysis: Extract key points → Generate summary → Create recommendations
- Code generation: Write specs → Generate code → Add documentation

---

## 2. Routing Pattern

### Description
Direct input to specialized sub-tasks based on classification or routing logic, ensuring separation of concerns. A router determines which specialized agent should handle the request.

### Workflow
```
Input -> Router → [Specialist Agent A | Specialist Agent B | Specialist Agent C] -> Output
```

### When to Use
- Different types of user queries requiring different expertise
- Multi-domain applications where specialized handling improves quality
- Resource optimization by directing simple queries to lighter models

### Example Use Cases
- Customer support: Route technical questions vs billing questions vs general inquiries
- Content classification: News articles → Topic-specific analyzers

---

## 3. Parallelization

### Description
Multiple prompts are executed in parallel, allowing for faster processing and improved efficiency. A coordinator dispatches work to multiple LLMs simultaneously, and an aggregator combines the results.

### Workflow
```
Input -> Coordinator -> [LLM1, LLM2, LLM3] (parallel execution) -> Aggregator -> Output
```

### Components
- **Coordinator**: Your code that manages the parallel execution of the LLMs
- **Aggregator**: Collects and combines results from parallel LLMs to produce the final output

### When to Use
- Independent sub-tasks that can be processed concurrently
- Time-sensitive applications requiring low latency
- Tasks benefiting from diverse perspectives or approaches
- Large-scale data processing

### Example Use Cases
- Multi-document summarization: Summarize each document in parallel, then aggregate
- Sentiment analysis across multiple data sources simultaneously
- Parallel translation to multiple languages

---

## 4. Orchestrator-Worker (Hierarchical)

### Description
Complex tasks are broken down into smaller sub-tasks by an orchestrator LLM, which assigns them to different specialized worker LLMs for processing. A synthesizer then aggregates the results.

### Workflow
```
Input -> Orchestrator (LLM) -> [Worker1, Worker2, Worker3] -> Synthesizer -> Output
```

### Components
- **Orchestrator**: An LLM that analyzes the task, creates a plan, and delegates to workers
- **Workers**: Specialized LLMs that handle specific sub-tasks
- **Synthesizer**: Combines worker outputs into a coherent final result

### When to Use
- Complex tasks requiring dynamic decomposition
- Tasks where the breakdown strategy isn't predetermined
- Multi-step problems requiring adaptive planning
- Scenarios needing specialized expertise for different components

### Example Use Cases
- Research projects: Orchestrator assigns literature review, data analysis, and writing tasks
- Software development: Plan features → Code components → Integrate and test
- Business analysis: Market research + competitor analysis + financial projections

---

## 5. Evaluator-Optimizer (Reflection)

### Description
LLM output is validated by another LLM acting as an evaluator. The evaluator provides feedback to the original LLM, which can then optimize its output based on the feedback received, creating an iterative improvement loop.

### Workflow
```
Input -> Generator (LLM) -> Evaluator (LLM) -> [Accept | Retry with Feedback] -> Output
```

### Process
1. Generator creates an initial output
2. Evaluator assesses quality and provides specific feedback
3. Generator refines output based on feedback (may iterate multiple times)
4. Final output is produced when quality criteria are met

### When to Use
- High-stakes outputs requiring quality assurance
- Tasks with well-defined success criteria
- Scenarios where iterative refinement improves results
- Complex reasoning requiring self-verification

### Example Use Cases
- Code generation with validation: Generate code → Check for bugs/style → Refine
- Creative writing: Draft content → Evaluate against guidelines → Improve
- Mathematical problem solving: Attempt solution → Verify correctness → Fix errors

---

## 6. Agent with Guardrails

### Description
An agent performs a specific task but operates within constraints enforced by guardrails. These guardrails ensure safe, ethical, and rule-compliant behavior by validating inputs, outputs, or agent actions.

### Workflow
```
Input -> [Input Validation] -> Agent -> [Output Validation] -> Output
```

### Guardrail Types
- **Input validation**: Check for malicious, inappropriate, or out-of-scope requests
- **Output validation**: Ensure responses meet safety, accuracy, and ethical standards
- **Action constraints**: Limit what actions an agent can take (e.g., API calls, data access)
- **Content filtering**: Remove sensitive information, PII, or harmful content

### When to Use
- Production applications requiring safety controls
- Regulated industries (healthcare, finance, legal)
- User-facing applications where harmful outputs must be prevented
- Systems with access to sensitive data or critical operations

### Example Use Cases
- Customer service chatbots with profanity filters and PII redaction
- Code assistants that prevent generation of malicious code
- Healthcare assistants ensuring HIPAA compliance
- Financial advisors with regulatory compliance checks

---

## 7. Agent with Custom Pydantic Models

### Description
An agent uses custom Pydantic models to structure and validate its input and output data. This ensures type safety, data validation, and clear API contracts.

### Workflow
```
Input (validated via Pydantic) -> Agent -> Output (validated via Pydantic)
```

### Benefits
- **Type Safety**: Catch errors early with strong typing
- **Validation**: Automatic data validation against schemas
- **Documentation**: Self-documenting APIs with clear data structures
- **Reliability**: Reduce runtime errors and unexpected data formats
- **Integration**: Easier integration with other systems expecting structured data

### When to Use
- Production systems requiring robust data validation
- Complex data structures with specific requirements
- API development with clear contracts
- Team collaborations needing shared data models
- Systems requiring audit trails and data lineage

### Example Use Cases
- Structured data extraction: Parse documents into predefined schemas
- API agents: Call external APIs with validated request/response models
- Database operations: Ensure data integrity before database writes
- Multi-agent systems: Standardize communication between agents

---

## Pattern Selection Guide

| Pattern | Complexity | Use Case | Key Benefit |
|---------|-----------|----------|-------------|
| Prompt Chaining | Low | Sequential tasks | Simple, predictable flow |
| Routing | Low-Medium | Multi-domain handling | Specialized expertise |
| Parallelization | Medium | Independent tasks | Speed and efficiency |
| Orchestrator-Worker | High | Complex, dynamic tasks | Adaptive planning |
| Evaluator-Optimizer | Medium | Quality-critical outputs | Iterative improvement |
| Agent with Guardrails | Medium | Safety-critical apps | Risk mitigation |
| Custom Pydantic Models | Low-Medium | Structured data | Type safety and validation |

---

## Combining Patterns

These patterns are not mutually exclusive and can be combined for more sophisticated systems:

- **Orchestrator-Worker + Guardrails**: Complex task decomposition with safety controls
- **Parallelization + Evaluator**: Fast processing with quality verification
- **Routing + Custom Models**: Specialized agents with structured I/O
- **Chaining + Evaluator**: Multi-step pipeline with validation at each stage

Choose patterns based on your specific requirements for speed, quality, safety, and complexity.