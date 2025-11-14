# tests/factories.py
from dataclasses import dataclass
from typing import List, Optional
import factory
from faker import Faker

fake = Faker()

@dataclass
class TestScenario:
    name: str
    input: str
    expected_output: str
    agent_instructions: str
    tools: List[str] = None

class ScenarioFactory(factory.Factory):
    class Meta:
        model = TestScenario
    
    name = factory.LazyFunction(lambda: f"Scenario_{fake.word()}")
    input = factory.LazyFunction(fake.sentence)
    expected_output = factory.LazyFunction(fake.paragraph)
    agent_instructions = factory.LazyFunction(
        lambda: f"You are a {fake.job()} assistant"
    )
    tools = factory.LazyFunction(
        lambda: [fake.word() for _ in range(random.randint(0, 3))]
    )

# Usage
test_scenarios = [ScenarioFactory() for _ in range(10)]