from sast.sast import SAST
import subprocess
import json

class CodeQL(SAST):
    def __init__(self) -> None:
        super().__init__()
    
    def __read_sarif(self, results_path):
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


    
    def execute(self, **kwargs):

        source_root = kwargs['source_root']
        database_path = kwargs['database_path']
        results_path = kwargs['results_path']

        # self.commands = [
        #     f"make -C {source_root} clean",
        #     f"codeql database create '{database_path}' --language=cpp --overwrite --source-root='{source_root}'",
        #     f"codeql database analyze '{database_path}' --format=sarif-latest --output={results_path}"
        # ]

        # for command in self.commands:
        #     print('executing:', command)
        #     subprocess.run(command, shell=True)
        #     print('===========================')
        
        return self.__read_sarif(results_path)
