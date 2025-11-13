# optimization/token_optimizer.py
import tiktoken

class TokenOptimizer:
    def __init__(self, model: str = "gpt-4"):
        self.encoder = tiktoken.encoding_for_model(model)
        self.max_tokens = 8000  # Leave room for response
    
    def optimize_prompt(self, prompt: str, context: str) -> str:
        """Optimize prompt to fit within token limits"""
        prompt_tokens = len(self.encoder.encode(prompt))
        context_tokens = len(self.encoder.encode(context))
        
        total_tokens = prompt_tokens + context_tokens
        
        if total_tokens <= self.max_tokens:
            return f"{prompt}\n\nContext: {context}"
        
        # Truncate context to fit
        available_tokens = self.max_tokens - prompt_tokens - 50  # Buffer
        context_parts = context.split('. ')
        
        optimized_context = ""
        current_tokens = 0
        
        for part in context_parts:
            part_tokens = len(self.encoder.encode(part))
            if current_tokens + part_tokens <= available_tokens:
                optimized_context += part + ". "
                current_tokens += part_tokens
            else:
                break
        
        return f"{prompt}\n\nContext (truncated): {optimized_context}"