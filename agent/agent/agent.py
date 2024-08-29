from abc import ABC, abstractmethod

from agent.code_context import context
from agent.prompt_augment import augment
from agent.rag import rag_engines
from llm import llm
from sast import sast
import typing




class Agent(ABC):
    
    def __init__(self,
                llm : llm.LLM_Chain,
                memory,
                tools : typing.List[sast.SAST] = None,
                context_providers : typing.Dict[str, context.ContextProvider] = None,
                promptAugmenters : typing.Dict[str, augment.PromptAugmenter] = None,
                ragEngines : typing.Dict[str, rag_engines.RagEngine] = None
        ) -> None:
        '''
        Constructor for LLM agent

        Args:

            llm_chains          (dict[str, llm.LLM])                            : a dictonary containing mappings of unique identifiers and LLM chains
            sast_tools          (list[sast.SAST], optional)                     : a dictonary containing mappings of unique identifiers and SAST tools
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
        self.llm = llm
        self.memory = memory
        self.tools = tools


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