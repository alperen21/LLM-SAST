from langchain_core.tools import tool
from sast.codeql import CodeQL

codeQL = CodeQL()


@tool
def execute_codeql(source_root, database_path, results_path) -> None:
    """
    Executes the CodeQL static analysis workflow on a C++ project.

    This function is a wrapper that invokes the `execute` method of the `CodeQL` class.
    It automates the process of performing Static Application Security Testing (SAST)
    using CodeQL. The workflow involves cleaning the source directory, creating a CodeQL 
    database from the provided source code, running an analysis to produce a SARIF results 
    file, and then processing the SARIF file to extract relevant security findings.

    Args:
        source_root (str): The root directory of the source code to be analyzed.
        database_path (str): The file path where the CodeQL database will be stored.
        results_path (str): The file path where the SARIF results will be saved.

    Returns:
        None: The function does not return a value but will execute the entire CodeQL 
        workflow and print the results of the analysis.

    Example:
        To use this function, simply provide the necessary paths and call the function:

        execute_codeql(
            source_root='/path/to/source',
            database_path='/path/to/database',
            results_path='/path/to/results.sarif'
        )

        and the printed output is:

            Tool: CodeQL 
            Rule ID: cpp/dangerous-cin
            Message: Use of 'cin' without specifying the length of the input may be dangerous.
            Severity: warning
            File: main.cpp
            Start Line: 13
            End Line: 13

            Rule ID: cpp/dangerous-cin
            Message: Use of 'cin' without specifying the length of the input may be dangerous.
            Severity: warning
            File: main.cpp
            Start Line: 17
            End Line: 17

    """
    codeQL.execute(
            source_root = source_root,
            database_path = database_path,
            results_path = results_path
        )