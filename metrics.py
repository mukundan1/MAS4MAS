# monitoring/metrics.py
from prometheus_client import Counter, Histogram, Gauge
import time

# Define metrics
agent_requests = Counter('agent_requests_total', 'Total agent requests', ['agent_name', 'status'])
agent_latency = Histogram('agent_request_duration_seconds', 'Agent request latency', ['agent_name'])
active_agents = Gauge('active_agents', 'Number of active agents')
token_usage = Counter('token_usage_total', 'Total tokens used', ['model', 'agent_name'])

class MetricsCollector:
    @staticmethod
    def record_request(agent_name: str, status: str):
        agent_requests.labels(agent_name=agent_name, status=status).inc()
    
    @staticmethod
    def record_latency(agent_name: str, duration: float):
        agent_latency.labels(agent_name=agent_name).observe(duration)
    
    @staticmethod
    def record_tokens(model: str, agent_name: str, tokens: int):
        token_usage.labels(model=model, agent_name=agent_name).inc(tokens)