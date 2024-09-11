import openai
import getpass
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import pprint
from langchain.agents import initialize_agent, AgentType, tool
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from langchain_core.messages.base import BaseMessage



class LLMOnly:
    def __init__(self, llm, tools, augmenter, llm_type):
        self.tokens_used = 0
        self.total_chain_invocations = 0
        self.llm_type = llm_type
        self.llm = llm
        self.augmenter = augmenter
    
    def predict(self, function_body):

        self.total_chain_invocations += 1

        augmented_prompt = self.augmenter.augment(function_body)

        if self.llm_type == 'gpt':
            with get_openai_callback() as cb:
                response = self.llm.invoke(augmented_prompt)
                self.tokens_used += cb.total_tokens
        
        else:
            response = self.llm.invoke(augmented_prompt)

        print(response.content, '\n')
        if "@@vulnerable@@" in response.content.lower():
            print('vulnerable')
            return 1
        else:
            print('not vulnerable')
            return 0
        

    def get_tokens_used(self):
        return {'tokens_used' : self.tokens_used, 'total_chain_invocations' : self.total_chain_invocations}
        