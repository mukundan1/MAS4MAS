"""
Main entry point for the Meta-Agentic System.
This system creates multi-agent systems using LLMs.
"""
from orchestrator import Orchestrator

def main():
    print("=" * 60)
    print("Meta-Agentic System")
    print("=" * 60)
    
    # Get user input
    user_prompt = input("\nWhat multi-agent system would you like to create?\n> ")
    
    # Create orchestrator and run workflow
    orchestrator = Orchestrator(max_loops=3)
    orchestrator.run_workflow(user_prompt)

if __name__ == "__main__":
    main()

