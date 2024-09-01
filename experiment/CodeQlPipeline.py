from experiment.pipeline import Pipeline
from sast.codeql import CodeQL
import os
from config import Config
from pprint import pprint
from agent.code_context.cpp import CppFunctionContextProvider
from experiment.juliet import JulietSingleExecutor
from pprint import pprint
from config import Config



class CodeQlPipeline(Pipeline):
    
    
    def __init__(self, repository_path) -> None:
        self.repository_path = repository_path
        
        self.codeql = CodeQL()  
        
        contextProvider = CppFunctionContextProvider()
        
        results = self.codeql.execute(
            source_root = repository_path, #TODO: Generalize naming
            results_path = os.path.join(repository_path,'results.sarif'),
            database_path = Config["database_path"] 
        )
        
        
        self.detected = list()
        for result in results:
            for location in result["result_info"]["locations"]:
                file_path = os.path.join(repository_path,location["file"])
                start_line = location["start_line"]
                end_line = location["end_line"]
                
                function_body = contextProvider.provide_context(file_path, start_line, end_line)
                

                self.detected.append(function_body)
        
        print(len(self.detected))
    
    def predict(self, file_path, function):
        
        labeled_vulnerable = False
        for detected_function in self.detected:
            if function in detected_function:
                labeled_vulnerable = True
                break
        
        # input()
        return labeled_vulnerable
    
    
