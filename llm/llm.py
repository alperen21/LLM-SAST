from abc import ABC, abstractmethod
from typing import Union, Optional, Dict, Any
from langchain_core.runnables import Runnable
from langchain.schema import BaseMessage, PromptValue
from langchain_core.memory import BaseMemory
from langchain.chains import ConversationChain

class LLM_Chain(ABC):
    
    def __init__(self, 
                llm : Union[Runnable[PromptValue, str], Runnable[PromptValue, BaseMessage]],
                llm_kwargs : Optional[Dict[str, Any]] = None,
                memory : Optional[BaseMemory] = None,
                verbose : bool = True) -> None:
        '''
        Constructor for LLM Chain

        Args:

            llm                     (Runnable)                     : Language model to call
            llm_kwargs              (dict[str, Any], optional)     : Kwarg arguments to be sent to the llm
            memory                  (BaseMemory)                   : Memory store.
            verbose                 (bool)                         : whether or not the output of the large language model should be verbose (default true)

        Returns:

            None
        '''
        super().__init__()

        if llm_kwargs is None:
            self.llm = llm 
        else:
            self.llm = llm(*llm_kwargs)
        

        self.memory = memory
        self.verbose = verbose

        self.chain = ConversationChain(
            llm = self.llm,
            memory = self.memory,
            verbose = self.verbose
        )
    
    @abstractmethod
    def invoke(self, prompt : str) -> Dict[str, Any]:
        '''
        Run large language model chain

        Args:

            prompt                   (str)                     : prompt to be sent to the LLM

        
        Returns:
            Response
        '''
        pass

