from abc import ABC, abstractmethod

from agent.code_context import context
from agent.prompt_augment import augment
from agent.rag import rag
from llm import llm
from sast import sast





class Agent(ABC):
    
    def __init__(self,
                llm_chains : dict[str, llm.LLM_Chain],
                sast_tools : dict[str, sast.SAST] = None,
                context_providers : dict[str, context.ContextProvider] = None,
                promptAugmenters : dict[str, augment.PromtAugmenter] = None,
                ragEngines : dict[str, rag.RagEngine] = None
        ) -> None:
        '''
        Constructor for LLM agent

        Args:

            llm_chains          (dict[str, llm.LLM])                            : a dictonary containing mappings of unique identifiers and LLM chains
            sast_tools          (dict[str, sast.SAST], optional)                : a dictonary containing mappings of unique identifiers and SAST tools
            context_providers   (dict[str, context.ContextProvider], optional)  : a dictonary containing mappings of unique identifiers and code context providers
            promptAugmenters    (dict[str, augment.PromtAugmenter], optional)   : a dictonary containing mappings of unique identifiers and prompt augmenter classes
            ragEngines          (dict[str, rag.RagEngine],  optional)           : a dictonary containing mappings of unique identifiers and rag engines

        Returns:

            None
        '''

        
        super().__init__()

        self.context_providers = context_providers
        self.promptAugmenters = promptAugmenters
        self.ragEngines = ragEngines
        self.llms = llm_chains
        self.sast_tools = sast_tools


    @abstractmethod
    def run(self, prompt : str) -> str:
        '''
        Run the LLM agent

        Args:

            prompt (str) : the prompt to run the LLM agent
            
        Returns:

            None
        '''
        pass