from typing import Any, Dict
from llm.llm import LLM_Chain
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory

class ChatGPT_LLM_Chain(LLM_Chain):

    def __init__(self, gpt_version = 'gpt-3.5-turbo-0125', verbose: bool = True) -> None:
        super().__init__(
            ChatOpenAI(model = gpt_version, max_tokens=1024, temperature=0), 
            None,
            ConversationBufferMemory(),
            verbose)
        
    
    def invoke(self, prompt : str) -> Dict[str, Any]:

        response = self.chain.run(prompt)

        return response

