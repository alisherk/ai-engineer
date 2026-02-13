# Agentic worflow design patterns 

1. Prompt chaining: The output of one prompt is used as the input for the next prompt. This allows for complex workflows to be built by chaining together multiple prompts.

2. Direct input into a specialized sub-tasks, ensuring separation of concerns. 

3. Parallelization: Multiple prompts can be executed in parallel, allowing for faster processing and improved efficiency.
   Input -> Coordinator -> [LLM1, LLM2, LLM3] -> Aggregator -> Output

   here coordinator is your code that manages the parallel execution of the LLMs, while the aggregator is responsible for collecting and combining the results from the LLMs to produce the final output.

4. Orchestration-Worker: Complex tasks are broken down into smaller sub-tasks, which are then assigned to different workers (LLMs) for processing. The synthesizer manages the workflow and ensures that the results from the workers are aggregated correctly.
   Input -> Orchestrator -> [Worker1, Worker2, Worker3] -> Synthesizer -> Output

   here orchestrator is LLM that manages the workflow, while workers are specialized LLMs that handle specific sub-tasks. The synthesizer is responsible for aggregating the results from the workers and producing the final output.

5. Evaluator-Optimizer: LLM output is validated by another LLM acting as an evaluator. The evaluator provides feedback to the original LLM,   which can then optimize its output based on the feedback received.
   Input -> LLM Generator -> LLM Evaluator (Optimization) -> Output

   here the LLM generates an initial output, which is then evaluated by the Evaluator. The Evaluator provides feedback on the quality of the output, and the LLM uses this feedback to optimize its response before producing the final output.



