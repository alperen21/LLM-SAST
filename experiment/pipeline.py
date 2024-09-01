from abc import ABC, abstractmethod


class Pipeline(ABC):
    
    def __init__(self, repository_path) -> None:
        super().__init__()
    
    @abstractmethod
    def predict(self, file_path, function):
        raise NotImplementedError