import openai
import getpass
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import pprint
from langchain.agents import initialize_agent, AgentType, tool
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
import subprocess
from langchain_core.messages.base import BaseMessage



class AgentToSast:
    def __init__(self, llm, tools, augmenter):
        self.agent = initialize_agent(
            tools=tools,  # List of tools the agent can use
            llm=llm,  # The language model
            agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Choose the type of agent
            verbose=True,  # Whether to print out the intermediate steps,
            handle_parsing_errors=True
        )
        self.augmenter = augmenter
    
    def predict(self, function_body):

        augmented_prompt = self.augmenter.augment(function_body)
        response = self.agent.run(augmented_prompt)
        
        if "@@vulnerable@@" in response.lower():
            return 1
        else:
            return 0
        