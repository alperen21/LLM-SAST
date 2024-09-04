from config import Config
import re
import os
import random
from pprint import pprint
import json
from config import Config   
import subprocess

class JulietBenchmark():
    def __init__(self):
        self.juliet_path = Config["juliet_path"]
        self.labeled_functions = self.__get_labeled_functions()
        self.index = 0
        
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
            return function_calls
        else:
            return []
    
    def __get_labeled_functions(self):
        
        vulnerable = self.__extract_functions(vulnerable_functions=True)
        non_vulnerable = self.__extract_functions(vulnerable_functions=False)
        
        
        
        vulnerable = [(func, "vulnerable") for func in vulnerable]
        non_vulnerable = [(func, "not vulnerable") for func in non_vulnerable] #TODO: Change with enum
        
        
        
        labeled_functions = vulnerable + non_vulnerable
        random.shuffle(labeled_functions)
        
        return labeled_functions
    
    def get_random_function(self):
        random_function = self.labeled_functions[self.index]
        
        self.index += 1
        
        return random_function


class PrimeVulBenchmark:
    
    def __init__(self):
        self.index = -1
        self.results = {
            1: { # ground truth / label
                 1: dict(), # prediction to CWE mappings
                 0: dict()
                },
            0: {
                    1: dict(),
                    0: dict()
            }
        }
        
        self.verbose_results = {
            1: { # ground truth / label
                 1: [], # prediction to CWE mappings
                 0: []
                },
            0: {
                    1: [],
                    0: []
            }
        }
        
        jsonl_file = os.path.join(Config["primevul_path"], "primevul_test.jsonl")

        with open("experiment/primevul_mapping.json", "r") as f:
            self.project_mappings = json.load(f) 

        self.data = []

        # Open the JSONL file and read line by line
        with open(jsonl_file, 'r') as file:
            for line in file:
                # Parse the JSON line into a dictionary
                self.data.append(json.loads(line))
    
    def get_data_size(self):
        return len(self.data)
    
    def extract_unique_projects(self):
        unique_projects = set()
        for item in self.data:
            if 'project' in item:
                unique_projects.add(item['project'])
        return list(unique_projects)

    
    def get_random_function(self):
        
        self.index += 1
        random_function = self.data[self.index]
        
        while (random_function["project"] not in self.project_mappings):
            self.index += 1
            random_function = self.data[self.index]

        if self.index >= len(self.data):
            return None
        
        function_body = random_function["func"]
        label = random_function["target"]
        project_name = random_function["project"]
        commit_id = random_function["commit_id"]  
        
        
        return function_body

    def clean_test_directory(self):
        target_directory = Config["test_path"]
        process = subprocess.run(f"rm -rf {target_directory}", shell=True)
        
        return process.returncode

    def clone_repository(self):    
        
        project_name = self.data[self.index]["project"] 
        project_link = self.project_mappings[project_name]
        target_directory = Config["test_path"]
        
        process = subprocess.run(f"git clone {project_link} {target_directory}", shell=True)
        
        return process.returncode

    def checkout_commit(self):
        commit_id = self.data[self.index]["commit_id"]
        target_directory = Config["test_path"]
        
        process = subprocess.run(f"cd {target_directory} && git checkout {commit_id}", shell=True)
        
        return process.returncode

    def compile_code(self):
        directory = Config["test_path"]
        
        """Compile the C++ project in the specified directory."""
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory")
            return
        
        # Check for Makefile
        if os.path.exists(os.path.join(directory, 'Makefile')):
            print("Makefile found. Running 'make'...")
            p = subprocess.run("make", cwd=directory)
            return p.returncode
        
        # Check for CMakeLists.txt (CMake project)
        if os.path.exists(os.path.join(directory, 'CMakeLists.txt')):
            print("CMake project found. Running CMake build process...")
            build_dir = os.path.join(directory, "build")
            os.subprocess.run(build_dir, exist_ok=True)
            p1 = subprocess.run("cmake ..", cwd=build_dir)
            p2 = subprocess.run("make", cwd=build_dir)
            return (p1.returncode or p2.returncode)

        # Check for Autotools-based project (configure script)
        if os.path.exists(os.path.join(directory, 'configure')):
            print("Autotools project found. Running configure and make...")
            p1 = subprocess.run("./configure", cwd=directory)
            p2 = subprocess.run("make", cwd=directory)
            return (p1.returncode or p2.returncode)

        
        print("No supported build system found (Makefile, CMake, Autotools).")

    def receive_prediction(self, prediction):
        
        label = self.data[self.index]["target"]
        cwe = self.data[self.index].get("cwe", "")
        
        self.results[label][prediction][cwe] = self.results[label][prediction].get(cwe, 0) + 1
        self.verbose_results[label][prediction].append(self.index)
    
    def get_results(self):
        # Dump self.results into a JSON file
        with open('results.json', 'w') as file:
            json.dump(self.results, file)
        
        # Dump self.verbose_results into a JSON file
        with open('verbose_results.json', 'w') as file:
            json.dump(self.verbose_results, file)
        
        