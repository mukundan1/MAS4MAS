from praisonaiagents.llm import ModelCapabilities
from praisonaiagents import Agent, Task, PraisonAIAgents

# Initialize model capabilities detector
capabilities = ModelCapabilities()

# Analyze available models
print("Available Models and Their Capabilities:")
print("=" * 50)

models = capabilities.list_models()
for model in models:
    caps = capabilities.get_capabilities(model)
    print(f"\n{model}:")
    print(f"  Context: {caps['max_context']} tokens")
    print(f"  Strengths: {', '.join(caps['strengths'])}")
    print(f"  Cost: ${caps['cost_per_1k_tokens']}/1k tokens")

# Compare models for specific task
task_requirements = {
    "type": "code_generation",
    "complexity": "high",
    "language": "python",
    "context_needed": 8000
}

best_model = capabilities.recommend_model(task_requirements)
print(f"\nBest model for task: {best_model}")

# # Create agent with capability-aware model selection
# smart_agent = Agent(
#     name="Capability-Aware Agent",
#     role="Adaptive AI Assistant",
#     goal="Use the best model based on task requirements",
#     instructions="Leverage model capabilities for optimal performance",
#     model_selector=capabilities
# )

# # Test with different task types
# coding_task = Task(
#     description="Write a complex Python algorithm for graph traversal",
#     expected_output="Optimized Python code with explanation",
#     agent=smart_agent,
#     task_type="coding"
# )

# analysis_task = Task(
#     description="Analyze 100-page financial report",
#     expected_output="Comprehensive financial analysis",
#     agent=smart_agent,
#     task_type="long_context_analysis"
# )

# creative_task = Task(
#     description="Write a creative short story",
#     expected_output="Engaging narrative",
#     agent=smart_agent,
#     task_type="creative_writing"
# )

# # Run workflow
# workflow = PraisonAIAgents(
#     agents=[smart_agent],
#     tasks=[coding_task, analysis_task, creative_task],
#     verbose=True
# )

# results = workflow.start()

# # Show capability matching results
# print("\nCapability Matching Results:")
# for task, model in capabilities.get_task_model_mapping().items():
#     print(f"{task}: {model}")