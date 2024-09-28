from langchain.callbacks import get_openai_callback
from agent.callback import get_token_usage_callback
from transformers import GPT2TokenizerFast  # Replace with the correct tokenizer for your model

class Agent:
    def __init__(self, llm_type):
        self.llm_type = llm_type 
        self.tokens_used = 0
        self.total_chain_invocations = 0
    
    def call_llm(self, prompt):
        raise NotImplementedError("This method should be implemented in the child class")
    
    def invoke_agent(self, prompt):
        if self.llm_type == 'gpt': #use get_openai_callback if the used llm type is gpt
            with get_openai_callback() as cb:
                response = self.llm.invoke(prompt)
                self.tokens_used += cb.total_tokens
                self.total_chain_invocations += 1
  
        else:
            tokenizer = GPT2TokenizerFast.from_pretrained('gpt2') 
            with get_token_usage_callback(tokenizer) as cb:
                response = self.llm.invoke(prompt)
                self.tokens_used += cb.total_tokens
                self.total_chain_invocations += 1

        return response 
    
    
    def get_tokens_used(self):
        """
        Returns a dictionary containing the tokens used and the total number of chain invocations.
        Returns:
            dict: A dictionary with the following keys:
                - 'tokens_used': The tokens used.
                - 'total_chain_invocations': The total number of chain invocations.
        """
        
        return {'tokens_used' : self.tokens_used, 'total_chain_invocations' : self.total_chain_invocations}
        

        