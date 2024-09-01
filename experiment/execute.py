
from abc import ABC, abstractmethod

class ExperimentExecutor(ABC):
    
    @abstractmethod
    def get_labels(self):
        raise NotImplementedError

    @abstractmethod
    def execute_experiment(self, pipeline):
        raise NotImplementedError
    
    @abstractmethod
    def get_results(self):
        raise NotImplementedError