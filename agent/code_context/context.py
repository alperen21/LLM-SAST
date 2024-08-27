from abc import ABC, abstractmethod


class ContextProvider(ABC):

    @abstractmethod
    def provide_context(self, file_path : str, start_row : int = None, end_row : int = None, start_column : int = None, end_column : int = None) -> str:
        '''
        Provides the code context with snippet extraction

        Args:
            file_path       (str)               : The path of the file
            start_row       (int, optional)     : Start row of the context provided by SAST
            end_row         (int, optional)     : Start row of the context provided by SAST
            start_column    (int, optional)     : Start row of the context provided by SAST
            end_column      (int, optional)     : Start row of the context provided by SAST

        
        Returns:
            string : the provided code context

        Raises:
            FileNotFoundError
        '''