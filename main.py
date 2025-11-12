

#----------------------------------------------------
#IMPORTS

#----------------------------------------------------


import os, json, asyncio, logging
from sys import implementation
from tabnanny import verbose
from dotenv import load_dotenv
from praisonaiagents import Agent, Task, PraisonAIAgents #, Tools
from duckduckgo_search import DDGS
from e2b_code_interpreter import Sandbox   

from praisonaiagents.tools import (
    execute_code, analyze_code, format_code,
    lint_code, disassemble_code
)


from praisonaiagents import (
    register_display_callback,
    error_logs
)


#----------------------------------------------------

#LOG DEF

#----------------------------------------------------





# Register a custom logger
def log_to_file(event_type, data):
    with open("agent_logs.txt", "a") as f:
        f.write(f"[{event_type}] {data}\n")

register_display_callback(log_to_file)

# Check for errors
errors = error_logs(agent_name="AnalysisAgent")
if errors:
    print(f"Found {len(errors)} errors", errors)


# Configure logging
logging.basicConfig(format='-%(levelname)s- %(message)s:%(asctime)s ')
logger = logging.getLogger(__name__)

load_dotenv()

# Access API key from environment variable
api_key = os.getenv("OPENAI_API_KEY") or input("Enter OpenAI (Compatible if using other models) API key: ")


#----------------------------------------------------
#TOOL DEF


#----------------------------------------------------




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
    

# async def parallel_tasks():
#     tasks = [agent1.task(), agent2.task()]
#     results = await asyncio.gather(*tasks)


#----------------------------------------------------
#CHAT DEF


#----------------------------------------------------






InteractiveChatAgent = Agent(
    name="InteractiveChatAgent",
    backstory="",
    goal="",
    instructions="""
    You are a conversational assistant. Always execute the tool create_chat_interface tool. You have access to the internet_search_tool tool. 
    You can use this tool to search the internet for information to provide with options to the user's prompt.
    Collect all the necessary information by the format below for proper high-level implementation plan.
    FORMAT GUIDELINES:
    - Programming Language: [JavaScript, Python]
    - Framework: Use the internet_search_tool by the choice of language
    - Implementation Type: [API, Web Application, Desktop Application, Mobile Application, CLI Application]
    - Deployment Type: [Local, Cloud]

    Output:
    - JSON Specification of each agent in the system

    """,
    verbose=True,
    markdown=True,
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key,# Pass API key securely
    tools=[create_chat_interface, internet_search_tool] 
)



#----------------------------------------------------
#AGENTS DEF

#with instructions
#----------------------------------------------------




PlannerAgent = Agent(
    name="PlannerAgent",
    role="Senior Project Manager",
    goal="Provide both low & high level of implementation plan",
    backstory="You are an expert at creating software requirements and implementation plan",
    # instructions="Create detailed requirements for the CoderAgent to write execution level programming code",
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key,
    reasoning_steps=3,
    tools=[internet_search_tool]  # Pass API key securely
)

CoderAgent = Agent(
    name="CoderAgent",
    role="Senior Python Developer",
    goal="Write executuable Python code that should be running in localhost.",
    backstory="Expert Python developer with strong coding skills",
    tools=[
        code_interpreter, execute_code, analyze_code, format_code,
        lint_code, disassemble_code
    ],
    verbose=True,
    # instructions="",
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key  # Pass API key securely
)

TesterAgent = Agent(
    name="TesterAgent",
    role="Senior Python Tester",
    goal="Provide test results to check whether to reimplement the user defined requirements or completed implementation",
    backstory="Expert Python Tester",
    # instructions="",
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key  # Pass API key securely
)

DeployerAgent = Agent(
    name="DeployerAgent",
    role="Localhost Deployer",
    goal="Deploy and ensure running the implementation in localhost",
    backstory="Expert in local machine deployment using Docker(-compose) or Kubernetes",
    # instructions="",
    llm="gpt-4o-mini",  # Using the specified model
    api_key=api_key,
    tools=[internet_search_tool]  # Pass API key securely
)




#----------------------------------------------------
#TASK DEF

#with goal & backstory
#----------------------------------------------------




loop_interactive_task = Task(
    name="loop_interactive_task",
    description="Gather all the necessary information to form an implementation plan and low-level definition of user requirements.",
    expected_output="Low-level requirements gathering for real time implementation planning",
    agent=InteractiveChatAgent,
    tools=[internet_search_tool()],
    
    retain_full_context=True,
    async_execution=True

    type="loop",
    
    operation="process_item"
)


planning_task = Task(
    name="planning_task"
    description="",
    expected_output="Provide a detailed implementation plan with the user specification plus requirements in JSON format",
    agent=PlannerAgent,
    tools=[internet_search_tool()],
    output_file="Planning.md",
    async_execution=True,

)

decision_task = Task(
    
    name="decision_task",
    description="Review all the user requirements are fulfilled or not for the next action",
    expected_output="Decision: approve, revise, or reject"
    context=[loop_interactive_task],
    task_type="decision",
    conditions={
        "approve": ["planner_task"],
        "revise": ["loop_interactive_task"],
        "reject": ["loop_interactive_task"]
    }
)


coding_task = Task(
    name="coding_task",
    description="Codes the provided implementation plan and user defined requirements",
    expected_output="Python code running in localhost in local machine",
    agent=CoderAgent,
    tools=[internet_search_tool()],
    output_file="Code.md",
    context=["planning_task"],

    # Pass API key securely
)

tester_task = Task(
    name="tester_task",
    description="Test the written code against the implementation/requirements plan",
    expected_output="Confidence level by test score against the written code",
    agent=TesterAgent,
    tools=[internet_search_tool()],
    output_file="Test.md",
    context=["planning_task", "coding_task"], # Pass API key securely
)



test_decision_task = Task(
    
    name="test_decision_task",
    description="Decision by the confidence level against implementation plan : approve or revise",
    expected_output="Decision: approve, or revise"
    context=[loop_interactive_task],
    task_type="decision",
    conditions={
        "approve": ["deployer_task"],
        "revise": ["loop_interactive_task"],
    }
)


deployer_task = Task(
    name="deployer_task",
    description="Deploys the system in localhost",
    expected_output="Running localhost of the written code in local machine",
    agent=DeployerAgent,
    tools=[internet_search_tool()],
    # output_file="Test.md",
    # context=["planning_task", "coding_task"], # Pass API key securely
)


#----------------------------------------------------
# TEAM DEF - MAIN
#----------------------------------------------------


# Create a multi-agent system
expert_team = PraisonAIAgents(
    agents=[ #InteractiveChatAgent, 
    PlannerAgent, CoderAgent, TesterAgent, DeployerAgent],
    tasks=[loop_interactive_task, planning_task, decision_task, coding_task],
    process="hierarchical",
    max_retries=3,
    manager_llm = "gpt-4",
    verbose=True  # Enables detailed logging
)

# Start the multi-agent system
response = expert_team.start()
print(response)

if __name__ == "__main__":
    create_chat_interface()
    expert_team.run_all_tasks()
    expert_team.get_all_tasks_status()