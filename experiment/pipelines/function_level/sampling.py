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



class SamplingPipeline:
    def __init__(self, llm, tools, augmenter, llm_type):
        self.tokens_used = 0
        self.total_chain_invocations = 0
        self.llm_type = llm_type
        self.llm = llm
        self.augmenter = augmenter
    
    def predict(self, function_body, sampling = 2):
        vulnerable_predictions = 0
        not_vulnerable_predictions = 0
        
        for i in range(sampling):
            prediction = self.predict_once(function_body)
            if prediction == 1:
                vulnerable_predictions += 1
            else:
                not_vulnerable_predictions += 1
                
            print("prediction:", i)
         
        print("vulnerable_predictions: ", vulnerable_predictions)
        print("not_vulnerable_predictions: ", not_vulnerable_predictions)       
        if vulnerable_predictions > not_vulnerable_predictions:
            return 1
        else:
            return 0
    
    def predict_once(self, function_body):

        self.total_chain_invocations += 1

        augmented_prompt = self.augmenter.augment(function_body)

        print(augmented_prompt[0].content)

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
        