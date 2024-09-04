from abc import ABC, abstractmethod
from typing import List
from langchain_core.messages.base import BaseMessage


class PromptAugmenter(ABC):

    @abstractmethod
    def augment(self, code : str) -> List[BaseMessage]:
        '''
        Provides the code context with snippet extraction

        Args:
            code       (str)               : Code to be added
            file_path       (str)          : File path of the code

        Returns:
            string : the augmented prompt
        '''

        