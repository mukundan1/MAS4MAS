# tests/debug_utils.py
import json
import pdb
from rich import print as rprint
from rich.table import Table

def debug_agent_state(agent):
    """Print agent state for debugging"""
    table = Table(title=f"Agent: {agent.name}")
    table.add_column("Property", style="cyan")
    table.add_column("Value", style="green")
    
    table.add_row("Instructions", agent.instructions[:50] + "...")
    table.add_row("Tools", str(len(agent.tools)))
    table.add_row("Memory Size", str(len(agent.memory.messages)))
    table.add_row("Model", agent.llm_model)
    
    rprint(table)

def trace_execution(func):
    """Decorator to trace function execution"""
    def wrapper(*args, **kwargs):
        print(f"Entering {func.__name__}")
        pdb.set_trace()
        result = func(*args, **kwargs)
        print(f"Exiting {func.__name__} with result: {result}")
        return result
    return wrapper