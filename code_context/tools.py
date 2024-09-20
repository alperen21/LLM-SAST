
from langchain_core.tools import tool
import subprocess
from config import Config
import os
from langchain.agents import Tool
from state import SharedState


# Define the tools
@tool("find_c_symbol", return_direct=True)
def find_c_symbol(symbol: str) -> str:
    """
    Find all references to a C symbol in the codebase.

    Args:
        symbol (str): The name of the C symbol to search for.

    Returns:
        str: The output from cscope containing all references to the symbol.
    """
    subprocess.run('find . \( -name "*.c" -o -name "*.cpp" -o -name "*.h" \) > cscope.files', cwd=Config["test_path"], shell=True, capture_output=True)
    subprocess.run('cscope -b -q -k', cwd=Config["test_path"], shell=True, capture_output=True)
    return subprocess.run(f'cscope -dL -0 {symbol}', cwd=Config["test_path"], shell=True, capture_output=True).stdout


@tool("find_global_definition", return_direct=True)
def find_global_definition(symbol: str) -> str:
    """
    Find the global definition of a symbol in the codebase.

    Args:
        symbol (str): The name of the symbol to find the definition for.

    Returns:
        str: The output from cscope containing the definition of the symbol.
    """
    state = SharedState()
    state.function_name = symbol
    subprocess.run('find . \( -name "*.c" -o -name "*.cpp" -o -name "*.h" \) > cscope.files', cwd=Config["test_path"], shell=True, capture_output=True)
    subprocess.run('cscope -b -q -k', cwd=Config["test_path"], shell=True, capture_output=True)
    return subprocess.run(f'cscope -dL -1 {symbol}', cwd=Config["test_path"], shell=True, capture_output=True).stdout



@tool("find_functions_called_by", return_direct=True)
def find_functions_called_by(function_name: str) -> str:
    """
    Find all functions that are called by a specified function.

    Args:
        function_name (str): The name of the function whose called functions are to be found.

    Returns:
        str: The output from cscope containing functions called by the specified function.
    """
    subprocess.run('find . \( -name "*.c" -o -name "*.cpp" -o -name "*.h" \) > cscope.files', cwd=Config["test_path"], shell=True, capture_output=True)
    subprocess.run('cscope -b -q -k', cwd=Config["test_path"], shell=True, capture_output=True)
    state = SharedState()
    state.function_name = function_name
    return subprocess.run(f'cscope -dL -2 {function_name}', cwd=Config["test_path"], shell=True, capture_output=True).stdout


@tool("find_functions_calling", return_direct=True)
def find_functions_calling(function_name: str) -> str:
    """
    Find all functions that call a specified function.

    Args:
        function_name (str): The name of the function whose callers are to be found.

    Returns:
        str: The output from cscope containing functions that call the specified function.
    """
    subprocess.run('find . \( -name "*.c" -o -name "*.cpp" -o -name "*.h" \) > cscope.files', cwd=Config["test_path"], shell=True, capture_output=True)
    subprocess.run('cscope -b -q -k', cwd=Config["test_path"], shell=True, capture_output=True)
    state = SharedState()
    state.function_name = function_name
    return subprocess.run(f'cscope -dL -3 {function_name}', cwd=Config["test_path"], shell=True, capture_output=True).stdout


@tool("find_text_string", return_direct=True)
def find_text_string(text: str) -> str:
    """
    Find all occurrences of a specified text string in the codebase.

    Args:
        text (str): The text string to search for.

    Returns:
        str: The output from cscope containing all occurrences of the text string.
    """
    subprocess.run('find . \( -name "*.c" -o -name "*.cpp" -o -name "*.h" \) > cscope.files', cwd=Config["test_path"], shell=True, capture_output=True)
    subprocess.run('cscope -b -q -k', cwd=Config["test_path"], shell=True, capture_output=True)
    return subprocess.run(f'cscope -dL -4 {text}', cwd=Config["test_path"], shell=True, capture_output=True).stdout


@tool("find_egrep_pattern", return_direct=True)
def find_egrep_pattern(pattern: str) -> str:
    """
    Find all lines matching a specified egrep pattern in the codebase.

    Args:
        pattern (str): The egrep pattern to search for.

    Returns:
        str: The output from cscope containing all lines matching the pattern.
    """
    subprocess.run('find . \( -name "*.c" -o -name "*.cpp" -o -name "*.h" \) > cscope.files', cwd=Config["test_path"], shell=True, capture_output=True)
    subprocess.run('cscope -b -q -k', cwd=Config["test_path"], shell=True, capture_output=True)
    return subprocess.run(f'cscope -dL -6 {pattern}', cwd=Config["test_path"], shell=True, capture_output=True).stdout


@tool("find_file", return_direct=True)
def find_file(file_name: str) -> str:
    """
    Find a specified file in the codebase.

    Args:
        file_name (str): The name of the file to find.

    Returns:
        str: The output from cscope containing the location of the file.
    """
    subprocess.run('find . \( -name "*.c" -o -name "*.cpp" -o -name "*.h" \) > cscope.files', cwd=Config["test_path"], shell=True, capture_output=True)
    subprocess.run('cscope -b -q -k', cwd=Config["test_path"], shell=True, capture_output=True)

    return subprocess.run(f'cscope -dL -7 {file_name}', cwd=Config["test_path"], shell=True, capture_output=True).stdout


@tool("find_including_files", return_direct=True)
def find_including_files(file_name: str) -> str:
    """
    Find all files that include a specified file.

    Args:
        file_name (str): The name of the file to find inclusions for.

    Returns:
        str: The output from cscope containing files that include the specified file.
    """
    subprocess.run('find . \( -name "*.c" -o -name "*.cpp" -o -name "*.h" \) > cscope.files', cwd=Config["test_path"], shell=True, capture_output=True)
    subprocess.run('cscope -b -q -k', cwd=Config["test_path"], shell=True, capture_output=True)
    return subprocess.run(f'cscope -dL -8 {file_name}', cwd=Config["test_path"], shell=True, capture_output=True).stdout


@tool("readfile", return_direct=True)
def readfile(filename: str) -> str:
    """
    Read the contents of a specified file along with a function

    Args:
        filename (str): The name of the file to read.
        function_name (str): The name of the function to extract from the file.


    Returns:
        str: The contents of the file.
    """
    state = SharedState()
    return subprocess.run(
        f'cat {filename}',
        shell=True,
        capture_output=True,
        cwd=Config["test_path"]
    ).stdout

tools = [
    Tool(
        name="find_c_symbol",
        func=find_c_symbol,
        description="Find all references to a C symbol."
    ),
    Tool(
        name="find_global_definition",
        func=find_global_definition,
        description="Find the global definition of a symbol."
    ),
    Tool(
        name="find_functions_called_by",
        func=find_functions_called_by,
        description="Find functions called by the specified function."
    ),
    Tool(
        name="find_functions_calling",
        func=find_functions_calling,
        description="Find functions that call the specified function."
    ),
    Tool(
        name="find_text_string",
        func=find_text_string,
        description="Find all occurrences of the specified text string."
    ),
    Tool(
        name="find_egrep_pattern",
        func=find_egrep_pattern,
        description="Find all lines matching the specified egrep pattern."
    ),
    Tool(
        name="find_file",
        func=find_file,
        description="Find the specified file in the codebase."
    ),
    Tool(
        name="find_including_files",
        func=find_including_files,
        description="Find all files that include the specified file."
    ),
    Tool(
        name="read file",
        func=readfile,
        description="read file contents"
    )
]