from contextlib import contextmanager
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from typing import Any, Dict, List

# Import the tokenizer that matches your LLM
from transformers import GPT2TokenizerFast  # Replace with the correct tokenizer for your model

# Custom callback handler to track token usage
class TokenUsageCallbackHandler(BaseCallbackHandler):
    """Callback handler to track token usage for LLMs."""
    def __init__(self, tokenizer):
        self.total_tokens = 0
        self.prompt_tokens = 0
        self.completion_tokens = 0
        self.tokenizer = tokenizer

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any
    ) -> None:
        """Called when the LLM starts processing."""
        # Count tokens in the prompts
        prompt_tokens = sum(
            len(self.tokenizer.encode(prompt)) for prompt in prompts
        )
        self.prompt_tokens += prompt_tokens
        self.total_tokens += prompt_tokens

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        """Called when the LLM finishes processing."""
        # Count tokens in the completions
        for generation in response.generations:
            for gen in generation:
                completion = gen.text
                completion_tokens = len(self.tokenizer.encode(completion))
                self.completion_tokens += completion_tokens
                self.total_tokens += completion_tokens

# Context manager for the callback
@contextmanager
def get_token_usage_callback(tokenizer):
    """Context manager to track token usage for LLMs."""
    callback = TokenUsageCallbackHandler(tokenizer)
    try:
        yield callback
    finally:
        pass  # No cleanup necessary
