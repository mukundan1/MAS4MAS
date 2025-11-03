# llm_api.py
"""
LLM Abstraction Layer to handle Google, OpenAI, and Anthropic APIs.
"""
import os
import google.generativeai as genai
from openai import OpenAI
from anthropic import Anthropic
from config import API_KEYS

# Configure clients
try:
    genai.configure(api_key=API_KEYS["google"])
    openai_client = OpenAI(api_key=API_KEYS["openai"])
    anthropic_client = Anthropic(api_key=API_KEYS["anthropic"])
except KeyError as e:
    print(f"Error: API key for {e} not found in config.py. Please add it.")
    exit()

# Models - easy to swap
MODELS = {
    "planner": "gemini-1.5-pro-latest",
    "coder": "gemini-1.5-pro-latest",
    "tester": "gemini-1.5-pro-latest"
}

def call_llm(model_name: str, system_prompt: str, user_prompt: str) -> str:
    """
    Calls the specified LLM with a unified interface.
    
    Args:
        model_name: The "logical" name (e.g., "planner")
        system_prompt: The role and instructions for the AI.
        user_prompt: The user's specific request.
        
    Returns:
        The text response from the LLM.
    """
    actual_model = MODELS.get(model_name)
    if not actual_model:
        raise ValueError(f"Invalid model name: {model_name}. Must be one of {MODELS.keys()}")

    print(f"[LLM Call] Using {model_name} ({actual_model})...")
    
    try:
        if "claude" in actual_model:
            # Anthropic (Claude)
            message = anthropic_client.messages.create(
                model=actual_model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_prompt}
                ]
            )
            return message.content[0].text

        elif "gpt" in actual_model:
            # OpenAI (GPT)
            response = openai_client.chat.completions.create(
                model=actual_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=4096
            )
            return response.choices[0].message.content

        elif "gemini" in actual_model:
            # Google (Gemini)
            model = genai.GenerativeModel(
                model_name=actual_model,
                system_instruction=system_prompt
            )
            response = model.generate_content(user_prompt)
            return response.text

    except Exception as e:
        print(f"Error calling LLM {model_name} ({actual_model}): {e}")
        return f"Error: {e}"

if __name__ == '__main__':
    # Test call
    test_response = call_llm("planner", "You are a helpful assistant.", "Hello!")
    print(f"Test response: {test_response}")