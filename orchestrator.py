# orchestrator.py
"""
The main Orchestrator that manages the state and flow of agents.
"""
import json
from agents import PlannerAgent, CoderAgent, TesterAgent, DeployerAgent

class Orchestrator:
    def __init__(self, max_loops: int = 3):
        self.state = {}
        self.max_loops = max_loops
        self.agents = [
            PlannerAgent(),
            CoderAgent(),
            TesterAgent(),
            # The DeployerAgent is called manually after the loop
        ]
        self.deployer = DeployerAgent()

    def run_workflow(self, user_prompt: str):
        """
        Runs the full agentic workflow from prompt to deployment.
        """
        self.state = {"user_prompt": user_prompt}
        
        # 1. Plan
        self.state = self.agents[0].run(self.state) # PlannerAgent
        if "error" in self.state:
            print(f"Workflow failed at Planning: {self.state['error']}")
            return

        # 2. Code & Test Loop
        for i in range(self.max_loops):
            print(f"\n--- Iteration {i + 1} ---")
            
            # 2a. Code
            self.state = self.agents[1].run(self.state) # CoderAgent
            if "error" in self.state:
                print(f"Workflow failed at Coding: {self.state['error']}")
                return

            # 2b. Test
            self.state = self.agents[2].run(self.state) # TesterAgent
            if "error" in self.state:
                print(f"Workflow failed at Testing: {self.state['error']}")
                return

            # 2c. Check for success
            if self.state.get("test_results", {}).get("success", False):
                print("Code passed all tests!")
                break
            else:
                print("Code failed tests. Sending back to Coder for refinement...")
                if i == self.max_loops - 1:
                    print(f"Failed to generate valid code after {self.max_loops} attempts.")
                    return

        # 3. Deploy
        self.state = self.deployer.run(self.state)
        if "error" in self.state:
            print(f"Workflow failed at Deployment: {self.state['error']}")
            return
            
        print("\n--- Workflow Complete ---")
        print(f"Final state: {json.dumps(self.state, indent=2, default=str)}")
