from sast.sast import SAST
import subprocess
import sys
import json
import os
from config import Config
import shutil
import experiment.benchmarks.function_level as function_level

class CodeQL(SAST):
    """
    Python Class wrapper to execute CodeQL
    """
    def __init__(self) -> None:
        super().__init__()
    
    def read_sarif(self, results_path : str) -> list[dict]:
        """
        Args:
            results_path (str): what is the path of results.sarif (or anything analogous with change in config file)

        Returns:
            list:   Returns a simplified summary since the results.sarif file prior to processing is very long. 
                    It is a list of results, each result being a dictionary object.
                    Each dictionary object has two keys, tool_info and results_info
                    tool_info contains the name of the tool and the version
                    results_info contains rule_id, message, severity and a list containing the location
        """
        #TODO: simplify this further, LLMs are more likely to hallucinate when presented with too much irrelevant information
        with open(results_path, 'r') as sarif_file:
            sarif_data = json.load(sarif_file)

        results_list = []

        for run in sarif_data.get('runs', []):
            tool = run['tool']['driver']
            tool_info = {
                "tool_name": tool['name'],
                "tool_version": tool.get('version', '')
            }

            for result in run.get('results', []):
                rule_id = result.get('ruleId')
                message = result['message']['text']
                level = result.get('level', 'warning')
                
                result_info = {
                    "rule_id": rule_id,
                    "message": message,
                    "severity": level,
                    "locations": []
                }

                for location in result.get('locations', []):
                    physical_location = location.get('physicalLocation', {})
                    artifact_location = physical_location.get('artifactLocation', {}).get('uri', 'Unknown')
                    region = physical_location.get('region', {})
                    
                    start_line = region.get('startLine', 'Unknown')
                    end_line = region.get('endLine', start_line)
                    
                    location_info = {
                        "file": artifact_location,
                        "start_line": start_line,
                        "end_line": end_line
                    }
                    
                    result_info["locations"].append(location_info)

                # Add the result info to the results list
                results_list.append({
                    "tool_info": tool_info,
                    "result_info": result_info
                })

        return results_list

    def run_command(self, command, cwd=None):
        """Run a system command and print its output."""
        try:
            result = subprocess.run(command, shell=True, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(result.stdout.decode())
        except subprocess.CalledProcessError as e:
            print(f"Error during command execution: {e.stderr.decode()}")
            
    
    def clean_previous_compilation(self, directory):
        """Clean previous compilation based on the build system."""
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory")
            return
        
        # Check for Makefile
        if os.path.exists(os.path.join(directory, 'Makefile')):
            print("Makefile found. Running 'make clean'...")
            try:
                self.run_command("make clean", cwd=directory)
            except Exception:
                print(self.run_command("rm -rf *.o", cwd=directory))
            return
        
        # Check for CMakeLists.txt (CMake project)
        if os.path.exists(os.path.join(directory, 'CMakeLists.txt')):
            print("CMake project found. Removing the 'build' directory...")
            build_dir = os.path.join(directory, "build")
            if os.path.exists(build_dir):
                shutil.rmtree(build_dir)
                print(f"Removed {build_dir}")
            else:
                print("No 'build' directory found.")
            return

        # Check for Autotools-based project (configure script)
        if os.path.exists(os.path.join(directory, 'configure')):
            print("Autotools project found. Running 'make clean'...")
            
            try:
                self.run_command("make clean", cwd=directory)
            except Exception:
                print(self.run_command("rm -rf *.o", cwd=directory))
            return
    
        
    def compile_project_with_codeql(self, source_root, database_path):
        """Compile the C++ project with CodeQL database extraction."""
        self.run_command(f"codeql database create '{database_path}' --language=cpp --overwrite --source-root='{source_root}'")

    
    def execute(self, **kwargs):
        """
        Executes CodeQL

        Returns:
            (tuple): returns (return code, processed sarif results)
        """

        source_root = kwargs['source_root']
        database_path = kwargs['database_path']
        results_path = kwargs['results_path']
        
        try:
            self.clean_previous_compilation(source_root)
            self.compile_project_with_codeql(source_root, database_path)

            command = f"codeql database analyze '{database_path}' --format=sarif-latest --output={results_path}"

            print('executing:', command)
            p = subprocess.run(command, shell=True)
            print('===========================')
            
            return (p.returncode, self.read_sarif(results_path))
        except Exception as e:
            print("Error happened during CodeQL execution") #TODO: some projects don't compile with CodeQL, need to remove them from the dataset
            return (-1 , None)
        
        
class CodeQLDummy(CodeQL):
    """
    A class created for faster experiments. 
    CodeQL takes a while to execute, especially for large codebases
    This class has exactly the same interface as CodeQL and inherits from it, 
    however it overrides the execute method to return pre-prepared results
    """
    def __init__(self) -> None:
        super().__init__()
    
    def execute(self, **kwargs): #TODO: change **kwargs
        """
        Simulates execution of CodeQL by accessing tracked commit and project strings to match a sarif file and then processes the contents of the file and returns them
        Returns:
            (tuple): returns (return code, processed sarif results)
        """
        commit = function_level.commit #TODO: maybe create a shared state instead?
        project = function_level.project
        
        results_sarif = os.path.join(Config["dummy_codeql_results"], f"test_{project}_{commit}.sarif")
        results = self.read_sarif(results_sarif)
        
        print(results)
        
        return (0, results)