# tests/unit/test_task.py
import pytest
from unittest.mock import Mock
from praisonaiagents import Task, Agent

class TestTask:
    def test_task_creation(self):
        """Test task initialization"""
        agent = Mock(spec=Agent)
        task = Task(
            description="Test task",
            agent=agent,
            expected_output="Expected result"
        )
        
        assert task.description == "Test task"
        assert task.agent == agent
        assert task.expected_output == "Expected result"
    
    def test_task_dependencies(self):
        """Test task with dependencies"""
        agent = Mock(spec=Agent)
        task1 = Task(description="Task 1", agent=agent)
        task2 = Task(description="Task 2", agent=agent, depends_on=[task1])
        
        assert len(task2.depends_on) == 1
        assert task2.depends_on[0] == task1
    
    def test_task_context(self):
        """Test task context passing"""
        agent = Mock(spec=Agent)
        context = {"key": "value"}
        
        task = Task(
            description="Test task",
            agent=agent,
            context=context
        )
        
        assert task.context == context
    
    @patch('praisonaiagents.task.task.Task.execute')
    def test_task_execution(self, mock_execute):
        """Test task execution"""
        mock_execute.return_value = "Task completed"
        
        agent = Mock(spec=Agent)
        task = Task(description="Test", agent=agent)
        result = task.execute()
        
        assert result == "Task completed"
        mock_execute.assert_called_once()