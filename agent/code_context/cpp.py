import re
from agent.code_context.context import ContextProvider
import clang.cindex
from pprint import pprint

clang.cindex.Config.set_library_file('/usr/local/opt/llvm/lib/libclang.dylib')

class CppFunctionContextProvider:
    def __init__(self) -> None:
        pass

    def __extract_function_cpp(self, file_path, line_number):
        index = clang.cindex.Index.create()
        translation_unit = index.parse(file_path)

        def find_function(node, line_number, file_path):
            """
            Recursively searches for the function declaration or method that contains the specified line number in the given file.

            :param node: The current AST node.
            :param line_number: The line number to search for.
            :param file_path: The path to the file being analyzed.
            :return: The function or method `Cursor` if found, otherwise None.
            """
            # Check if the node is a function or method and matches the given file path
            if (node.kind == clang.cindex.CursorKind.FUNCTION_DECL or
                node.kind == clang.cindex.CursorKind.CXX_METHOD) and node.extent.start.file.name == file_path:
                
                # Check if the line number is within the function's extent
                if node.extent.start.line <= line_number <= node.extent.end.line:
                    return node

            # Recursively search the children nodes
            for child in node.get_children():
                result = find_function(child, line_number, file_path)
                if result:
                    return result
            
            return None

        # Start searching for the function in the translation unit
        function_node = find_function(translation_unit.cursor, line_number, file_path)

        if function_node is None:
            return None

        # Extract the source code for the function, including the signature
        with open(file_path, 'r') as file:
            lines = file.readlines()

        start_line = function_node.extent.start.line - 1
        end_line = function_node.extent.end.line

        # Return the full function signature and body
        return ''.join(lines[start_line:end_line])



    def provide_context(self, file_path : str, start_row : int = None, end_row : int = None, start_column : int = None, end_column : int = None) -> str:
        return self.__extract_function_cpp(file_path, start_row)

# Example usage:
# provider = CppFunctionContextProvider()
# function_source = provider.get_function_source('example.cpp', 42)
# print(function_source)