import os, json, asyncio
from tabnanny import verbose
from dotenv import load_dotenv
from praisonaiagents import Agent, Task, PraisonAIAgents
from duckduckgo_search import DDGS
from e2b_code_interpreter import Sandbox
# Load environment variables from .env file
load_dotenv()

# Access API key from environment variable
api_key = os.getenv("OPENAI_API_KEY") or input("Enter OpenAI (Compatible if using other models) API key: ")



# 1. Define the tool
def internet_search_tool(query: str):
    results = []
    ddgs = DDGS()
    for result in ddgs.text(keywords=query, max_results=5):
        results.append({
            "title": result.get("title", ""),
            "url": result.get("href", ""),
            "snippet": result.get("body", "")
        })
    return results


def code_interpreter(code: str):
    print(f"\n{'='*50}\n> Running following AI-generated code:\n{code}\n{'='*50}")
    exec_result = Sandbox().run_code(code)
    if exec_result.error:
        print("[Code Interpreter error]", exec_result.error)
        return {"error": str(exec_result.error)}
    else:
        results = []
        for result in exec_result.results:
            if hasattr(result, '__iter__'):
                results.extend(list(result))
            else:
                results.append(str(result))
        logs = {"stdout": list(exec_result.logs.stdout), "stderr": list(exec_result.logs.stderr)}
        return json.dumps({"results": results, "logs": logs})


def create_chat_interface():
    # Initialize agent

    
    print("Chat with AI Assistant (type 'exit' to quit)")
    print("-" * 50)
    
    # Start conversation
    conversation_active = True
    first_message = True
    
    while conversation_active:
        # Get user input
        user_message = input("You: ")
        
        # Check if user wants to exit
        if user_message.lower() == 'exit':
            print("Goodbye!")
            conversation_active = False
            continue
        
#         # Get agent response
#         try:
#             if first_message:
#                 response = agent.start(user_message)
#                 first_message = False
#             else:
#                 response = agent.continue(user_message)
            
#             print("\nAssistant:", response)
#             print("\n" + "-" * 50)
#         except Exception as e:
#             print(f"Error: {str(e)}")
    

async def parallel_tasks():
    tasks = [agent1.task(), agent2.task()]
    results = await asyncio.gather(*tasks)


InteractiveChatAgent = Agent(
    name="InteractiveChatAgent",
    backstory="",
    goal="",
    instructions="""
    You are a conversational assistant. Always execute the tool create_chat_interface tool. You have access to the internet_search_tool tool. 
    You can use this tool to search the internet for information to provide with options to the user's prompt.
    You are given a user prompt and you need to create a JSON specification of the multi-agent system.

    FORMAT GUIDELINES:
    - Programming Language: []
    - Framework: []
    - Implementation Type: [API, Web Application, Desktop Application, Mobile Application, CLI Application]
    - Deployment Type: [Local, Cloud]

    Output:
    - JSON Specification of the multi-agent system

    """,
    verbose=True,
    markdown=True,
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key,# Pass API key securely
    tools=[create_chat_interface, internet_search_tool] 
)

PlannerAgent = Agent(
    name="PlannerAgent",
    instructions="",
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key,
    tools=[internet_search_tool]  # Pass API key securely
)

CoderAgent = Agent(
    name="CoderAgent",
    role="Code Developer",
    goal="Write and execute Python code",
    backstory="Expert Python developer with strong coding skills",
    tools=[code_interpreter],
    verbose=True
    instructions="",
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key  # Pass API key securely
)

TesterAgent = Agent(
    name="TesterAgent",
    instructions="",
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key  # Pass API key securely
)

DeployerAgent = Agent(
    name="DeployerAgent",
    instructions="",
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key,
    tools=[internet_search_tool]  # Pass API key securely
)

loop_interactive_task = Task(
    name="planning"
    description="",
    expected_output="Detailed plan has to be made by the format given",
    agent=InteractiveChatAgent,
    tools=[internet_search_tool()],
    
    async_execution=True

    type="loop",
    
    operation="process_item"
)


planning_task = Task(
    name="planning"
    description="",
    expected_output="Detailed plan in JSON format",
    agent=PlannerAgent,
    tools=[internet_search_tool()],
    output_file="Planning.md",
    async_execution=True
)

decision_task = Task(
    type="decision",
    name="decision",
    context=[info_gather_task],
    conditions={
        "success": ["planner_task"],
        "failure": ["loop_interactive_task"]
    }
)


coding_task = Task(
    name="coding",
    description="",
    expected_output="",
    agent=CoderAgent,
    tools=[internet_search_tool()],
    output_file="Code.md",
    context=["planning_task"],

    # Pass API key securely
)

# Create a multi-agent system
expert_team = PraisonAIAgents(
    agents=[InteractiveChatAgent, PlannerAgent, CoderAgent, TesterAgent, DeployerAgent],
    process="hierarchical",
    verbose=True  # Enables detailed logging
)

# Start the multi-agent system
response = expert_team.start()
print(response)

if __name__ == "__main__":
    create_chat_interface()