from sast.sast import SAST
import subprocess
import json

class CodeQL(SAST):
    def __init__(self) -> None:
        super().__init__()
    
    def __read_sariff(self, results_path):
        with open(results_path, 'r') as sarif_file:
            sarif_data = json.load(sarif_file)

        # Extract and print information
        for run in sarif_data.get('runs', []):
            tool = run['tool']['driver']
            print(f"Tool: {tool['name']} {tool.get('version', '')}")
            
            for result in run.get('results', []):
                rule_id = result.get('ruleId')
                message = result['message']['text']
                level = result.get('level', 'warning')
                
                print(f"Rule ID: {rule_id}")
                print(f"Message: {message}")
                print(f"Severity: {level}")
                
                for location in result.get('locations', []):
                    physical_location = location.get('physicalLocation', {})
                    artifact_location = physical_location.get('artifactLocation', {}).get('uri', 'Unknown')
                    region = physical_location.get('region', {})
                    
                    start_line = region.get('startLine', 'Unknown')
                    end_line = region.get('endLine', start_line)
                    
                    print(f"File: {artifact_location}")
                    print(f"Start Line: {start_line}")
                    print(f"End Line: {end_line}")
                    print()


    
    def execute(self, **kwargs):

        source_root = kwargs['source_root']
        database_path = kwargs['database_path']
        results_path = kwargs['results_path']

        self.commands = [
            f"make -C {source_root} clean",
            f"codeql database create '{database_path}' --language=cpp --overwrite --source-root='{source_root}'",
            f"codeql database analyze '{database_path}' --format=sarif-latest --output={results_path}"
        ]

        for command in self.commands:
            print('executing:', command)
            subprocess.run(command, shell=True)
            print('===========================')
        
        self.__read_sariff(results_path)
