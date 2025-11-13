# tests/mocks/tool_mock.py
class MockTool:
    def __init__(self, name: str, return_value: Any = None, side_effect: Any = None):
        self.name = name
        self.return_value = return_value
        self.side_effect = side_effect
        self.call_count = 0
        self.call_args_list = []
    
    def execute(self, **kwargs):
        self.call_count += 1
        self.call_args_list.append(kwargs)
        
        if self.side_effect:
            if isinstance(self.side_effect, Exception):
                raise self.side_effect
            return self.side_effect(**kwargs)
        
        return self.return_value or f"Mock result from {self.name}"

# Usage
mock_search = MockTool(
    name="search",
    return_value="Search results for your query"
)

mock_calculator = MockTool(
    name="calculator",
    side_effect=lambda expression: eval(expression)
)