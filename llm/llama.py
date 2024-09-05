from typing import Any, Dict
from llm.llm import LLM_Chain
from langchain_ollama import ChatOllama
from langchain.memory import ConversationBufferMemory

class Llama_LLM_Chain(LLM_Chain):

    def __init__(self, llama_version = 'gpt-3.5-turbo-0125', verbose: bool = True) -> None:
        super().__init__(
            ChatOllama(model = llama_version, temperature=0), 
            None,
            ConversationBufferMemory(),
            verbose)
        
    
    def invoke(self, prompt : str) -> Dict[str, Any]:

        response = self.chain.run(prompt)

        return response

