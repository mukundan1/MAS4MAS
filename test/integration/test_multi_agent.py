# tests/integration/test_multi_agent.py
import pytest
from praisonaiagents import Agent, Task, PraisonAIAgents

class TestMultiAgentIntegration:
    @pytest.mark.integration
    def test_agent_collaboration(self, mock_llm):
        """Test multiple agents working together"""
        researcher = Agent(
            name="Researcher",
            instructions="Research the topic",
            llm=mock_llm
        )
        
        writer = Agent(
            name="Writer",
            instructions="Write based on research",
            llm=mock_llm
        )
        
        # Create tasks
        research_task = Task(
            description="Research AI trends",
            agent=researcher,
            expected_output="Research findings"
        )
        
        writing_task = Task(
            description="Write article on AI trends",
            agent=writer,
            depends_on=[research_task],
            expected_output="Article"
        )
        
        # Create workflow
        workflow = PraisonAIAgents(
            agents=[researcher, writer],
            tasks=[research_task, writing_task]
        )
        
        # Execute workflow
        result = workflow.start()
        
        assert result is not None
        assert len(workflow.results) == 2
    
    @pytest.mark.integration
    async def test_async_agent_workflow(self, mock_llm):
        """Test asynchronous multi-agent workflow"""
        agents = [
            Agent(name=f"Agent{i}", instructions=f"Process part {i}", llm=mock_llm)
            for i in range(3)
        ]
        
        tasks = [
            Task(description=f"Task {i}", agent=agents[i])
            for i in range(3)
        ]
        
        workflow = PraisonAIAgents(agents=agents, tasks=tasks)
        results = await workflow.astart()
        
        assert len(results) == 3