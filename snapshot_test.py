# tests/test_snapshots.py
import pytest
from syrupy import snapshot

def test_agent_output_snapshot(test_agent, snapshot):
    result = test_agent.run("Generate a report")
    assert result == snapshot