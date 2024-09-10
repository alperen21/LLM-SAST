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



class AgentToSast:
    """
    Pipeline that creates a ReAct agent with SAST tools introduced as LangChain tools
    Agent implementation in this is therefore compiled in a cyclic graph of 
        START ----> Agent Node ----> Decision Node  --invoke tool--> Tool Node --Recursive--> Agent Node
                                        --make decision--> END
    Therefore the pipeline is called "AgentToSast"
    """
    #TODO: Change Naming to LLM2SAST to better reflect the nature of the pipeline
    def __init__(self, llm, tools, augmenter, llm_type):
        self.tokens_used = 0 # Keeps track of the total number of tokens used
        self.total_chain_invocations = 0 # Keeps track of the total chain invocations, chain invocation refering to how many times the LLM node is visited in the traversal of the Acylic Graph
        self.llm_type = llm_type

        self.agent = initialize_agent(
            tools=tools,  # List of tools the agent can use
            llm=llm,  # The language model
            agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # Choose the type of agent
            verbose=True,  # Whether to print out the intermediate steps,
            handle_parsing_errors=True
        ) #TODO: LangChain's initialize_agent is now deprecated, migrate the codebase
        self.augmenter = augmenter
    
    def predict(self, function_body : str) -> int:
        """
        Predicts if the given function is vulnerable or not

        Args:
            function_body (str): the function body under test

        Returns:
            int: 1 if vulnerable, 0 if not vulnerable
        """
        
        #TODO: Change 1 and 0 to booleans

        self.total_chain_invocations += 1

        augmented_prompt = self.augmenter.augment(function_body)

        if self.llm_type == 'gpt': #use get_openai_callback if the used llm type is gpt
            with get_openai_callback() as cb:
                response = self.agent.invoke(augmented_prompt)
                self.tokens_used += cb.total_tokens
        
        else:
            response = self.agent.invoke(augmented_prompt)


        if "@@vulnerable@@" in response["output"].lower():
            print('vulnerable')
            return 1
        else:
            print('not vulnerable')
            return 0
        

    def get_tokens_used(self):
        """
        Returns a dictionary containing the tokens used and the total number of chain invocations.
        Returns:
            dict: A dictionary with the following keys:
                - 'tokens_used': The tokens used.
                - 'total_chain_invocations': The total number of chain invocations.
        """
        
        return {'tokens_used' : self.tokens_used, 'total_chain_invocations' : self.total_chain_invocations}
        
