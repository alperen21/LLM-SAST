from config import Config
import re
import os
import random
from pprint import pprint
import json
from config import Config   
import subprocess

class PrimeVulBenchmark:
    
    def __init__(self, output_identifier = ''):
        self.index = -1
        self.result_dir = os.path.join("PrimeVul", output_identifier)
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
        
        self.balance_targets()


    def get_data_size(self):
        return len(self.data)
    
    def balance_targets(self):
        random.seed(42)
        # Separate objects by target value
        target_0 = [obj for obj in self.data if obj.get('target') == 0]
        target_1 = [obj for obj in self.data if obj.get('target') == 1]

        # Determine the smaller group size
        smaller_size = min(len(target_0), len(target_1))

        # Shuffle both groups to randomize the selection
        random.shuffle(target_0)
        random.shuffle(target_1)

        # Select the number of items from each group equal to the smaller size
        balanced_data = target_0[:smaller_size] + target_1[:smaller_size]

        # Shuffle the balanced data
        random.shuffle(balanced_data)

        self.data = balanced_data


    
    def extract_unique_projects(self):
        unique_projects = set()
        for item in self.data:
            if 'project' in item:
                unique_projects.add(item['project'])
        return list(unique_projects)

    
    def get_random_function(self):
        
        self.index += 1
        
        
        if self.index >= len(self.data):
            return None
        
        random_function = self.data[self.index]
        
        while (random_function["project"] not in self.project_mappings):
            self.index += 1
            
            if self.index >= len(self.data):
                return None
            
            random_function = self.data[self.index]

        
        function_body = random_function["func"]
        
        
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
        
        label = int(self.data[self.index]["target"])

        cwe = str(self.data[self.index].get("cwe", ""))
        
        self.results[label][prediction][cwe] = self.results[label][prediction].get(cwe, 0) + 1
        self.verbose_results[label][prediction].append(self.index)
    
    def get_results(self):
        
        if not os.path.exists(self.result_dir):
            os.makedirs(self.result_dir)
            
        # Dump self.results into a JSON file
        with open(os.path.join(self.result_dir, 'results.json'), 'w') as file:
            json.dump(self.results, file)
        
        # Dump self.verbose_results into a JSON file
        with open(os.path.join(self.result_dir, 'verbose_results.json'), 'w') as file:
            json.dump(self.verbose_results, file)
        
    
    def get_corresponding_repo(self):
        
        if self.index >= len(self.data):
            return None
        
        project_name = self.data[self.index]["project"]
        repo_link = self.project_mappings[project_name]

        return repo_link


commit = str()
project = str()
class PrimeVulBenchmarkDummy(PrimeVulBenchmark):
    def get_random_function(self):
        global commit
        global project 
        
        
        result = super().get_random_function()
        while (self.data[self.index]["commit_id"] not in Config["dummy_codeql_commits"]):
            result = super().get_random_function()
            
            if result is None:
                return None
        
        commit = self.data[self.index]["commit_id"]
        project = self.data[self.index]["project"]
        
        return result