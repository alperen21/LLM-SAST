import re
from agent.code_context.context import ContextProvider

class CppFunctionContextProvider(ContextProvider):
    def __init__(self) -> None:
        super().__init__()

    def __extract_function_cpp(self, file_path, line_number):
        with open(file_path, 'r') as file:
            lines = file.readlines()

        function_pattern = re.compile(r'^[\w\s:*&]+[\w\s:*&]+\([\w\s,.*&]*\)\s*{')
        function_start = None
        brace_count = 0

        for i, line in enumerate(lines):
            if function_start is None and function_pattern.match(line):
                function_start = i
                brace_count = line.count('{') - line.count('}')
            elif function_start is not None:
                brace_count += line.count('{') - line.count('}')
                if brace_count == 0:
                    if function_start <= line_number - 1 <= i:
                        return function_start, i
                    function_start = None

        return None

    def provide_context(self, file_path : str, start_row : int = None, end_row : int = None, start_column : int = None, end_column : int = None) -> str:
        extent = self.__extract_function_cpp(file_path, start_row)
        if extent is None:
            return None

        start_line, end_line = extent
        with open(file_path, 'r') as file:
            lines = file.readlines()
            function_lines = lines[start_line:end_line + 1]
            return ''.join(function_lines)

# Example usage:
# provider = CppFunctionContextProvider()
# function_source = provider.get_function_source('example.cpp', 42)
# print(function_source)