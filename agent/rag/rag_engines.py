from abc import ABC, abstractmethod


class RagEngine(ABC):
    
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def get_relevant_chunks(self, question: str, context: str) -> str:
        raise NotImplementedError