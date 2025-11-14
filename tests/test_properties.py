# tests/test_properties.py
from hypothesis import given, strategies as st

@given(st.text(min_size=1, max_size=1000))
def test_agent_handles_any_text_input(test_agent, text):
    result = test_agent.run(text)
    assert result is not None
    assert isinstance(result, str)
    assert len(result) > 0