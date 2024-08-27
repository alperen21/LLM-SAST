from abc import ABC, abstractmethod


class SAST(ABC):
    
    def __init__(self) -> None:
        super().__init__()
    
    @abstractmethod
    def execute(self, **kwargs):
        pass