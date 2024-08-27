from abc import ABC, abstractmethod


class PromtAugmenter(ABC):

    @abstractmethod
    def augment(self, prompt : str) -> str:
        '''
        Provides the code context with snippet extraction

        Args:
            prompt       (str)               : Prompt that will be augmented

        Returns:
            string : the augmented prompt
        '''

        