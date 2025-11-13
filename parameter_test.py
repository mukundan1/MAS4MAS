@pytest.mark.parametrize("input,expected", [
    ("Hello", "Hi there!"),
    ("How are you?", "I'm doing well!"),
    ("Goodbye", "See you later!"),
])
def test_agent_responses(test_agent, input, expected):
    result = test_agent.run(input)
    assert expected in result