# optimization/model_selector.py
from typing import Dict, Optional

class CostOptimizedModelSelector:
    def __init__(self):
        self.model_costs = {
            "gpt-4": 0.03,
            "gpt-3.5-turbo": 0.002,
            "claude-3-opus": 0.015,
            "claude-3-sonnet": 0.003
        }
        self.model_capabilities = {
            "gpt-4": ["complex_reasoning", "code", "analysis"],
            "gpt-3.5-turbo": ["general", "conversation"],
            "claude-3-opus": ["complex_reasoning", "long_context"],
            "claude-3-sonnet": ["general", "fast"]
        }
    
    def select_model(self, task_type: str, max_cost: Optional[float] = None) -> str:
        """Select most cost-effective model for task"""
        suitable_models = [
            model for model, capabilities in self.model_capabilities.items()
            if task_type in capabilities or "general" in capabilities
        ]
        
        if max_cost:
            suitable_models = [
                model for model in suitable_models
                if self.model_costs[model] <= max_cost
            ]
        
        # Return cheapest suitable model
        return min(suitable_models, key=lambda m: self.model_costs[m])