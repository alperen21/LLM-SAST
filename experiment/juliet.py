from experiment.execute import ExperimentExecutor
from config import Config
import re
import os
import random

class JulietSingleExecutor(ExperimentExecutor):
    def __init__(self):
        self.juliet_path = Config["juliet_path"]
        
    def __extract_functions(self, vulnerable_functions = True):
        with open(os.path.join(self.juliet_path, "main.cpp"), 'r') as file:
            content = file.read()
        
        signifier = 'OMITBAD' if vulnerable_functions else 'OMITGOOD'

        # Regular expression to match function calls within the OMITGOOD block, excluding printLine
        pattern = re.compile(f"#ifndef {signifier}\s*(.*?)\s*#endif \/\* {signifier} \*\/", re.DOTALL)
        match = pattern.search(content)

        if match:
            block = match.group(1)
            # Extract function calls, exclude printLine
            function_calls = re.findall(r'Calling (CWE.*);"', block)
            # Remove duplicates and return the function names
            return list(function_calls)
        else:
            return []
    def __sample_dict(self, data_dict, fraction):
        sampled_dict = {}
        
        for key, value_list in data_dict.items():
            sample_size = max(1, int(len(value_list) * fraction))  # Calculate 1/5th (or fraction) of the list size
            sampled_dict[key] = random.sample(value_list, sample_size)  # Randomly sample the elements
        
        return sampled_dict
    def get_labels(self):
        
        self.labels = {
            "vulnerable" : self.__extract_functions(vulnerable_functions=True),
            "non_vulnerable" : self.__extract_functions(vulnerable_functions=False),
        }
        
        return self.labels
    
    def execute_experiment(self, pipeline, execute_ratio = 1.0):
        experiment_dict = self.__sample_dict(self.labels, execute_ratio)
        
        vulnerable_functions = experiment_dict["vulnerable"]
        non_vulnerable_functions = experiment_dict["non_vulnerable"]
        
        correct_vulnerable_predictions = 0
        for function in vulnerable_functions:
            labeled_vulnerable = pipeline.predict(os.path.join(self.juliet_path, "main.cpp"), function)
            
            if labeled_vulnerable:
                correct_vulnerable_predictions += 1
        
        correct_non_vulnerable_predictions = 0
        for function in non_vulnerable_functions:
            labeled_vulnerable = pipeline.predict(os.path.join(self.juliet_path, "main.cpp"), function)
            
            if not labeled_vulnerable:
                correct_non_vulnerable_predictions += 1
            
        self.results = {
            "correct_vulnerable_predictions" : correct_vulnerable_predictions,
            "correct_non_vulnerable_predictions" : correct_non_vulnerable_predictions,
            "total_vulnerable_functions" : len(vulnerable_functions),
            "total_non_vulnerable_functions" : len(non_vulnerable_functions)
        }

    
    def get_results(self):
        return self.results