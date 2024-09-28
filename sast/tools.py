from langchain_core.tools import tool
from sast.codeql import CodeQL, CodeQLDummy
from config import Config   
import os
import subprocess
import sys


codeQL = CodeQL()
codeQLDummy = CodeQLDummy()

@tool
def execute_dummy_codeql(function_body) -> None:
    """
    Executes the CodeQL static analysis workflow on a C++ project.

    It automates the process of performing Static Application Security Testing (SAST)
    using CodeQL. The workflow involves cleaning the source directory, creating a CodeQL 
    database from the provided source code, running an analysis to produce a SARIF results 
    file, and then processing the SARIF file to extract relevant security findings.


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
    source_root = Config["test_path"]
    database_path = os.path.join(source_root, "codeql-db")
    results_path = os.path.join(source_root, "results.sarif")
    
    _, result = codeQLDummy.execute(
        source_root=source_root,
        database_path=database_path,
        results_path=results_path
    )
    
    result = codeQLDummy.extract_relevant_results(result, function_body)
    return result

@tool
def execute_codeql(input_str) -> None:
    """
    Executes the CodeQL static analysis workflow on a C++ project.

    It automates the process of performing Static Application Security Testing (SAST)
    using CodeQL. The workflow involves cleaning the source directory, creating a CodeQL 
    database from the provided source code, running an analysis to produce a SARIF results 
    file, and then processing the SARIF file to extract relevant security findings.


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
    source_root = Config["test_path"]
    database_path = os.path.join(source_root, "codeql-db")
    results_path = os.path.join(source_root, "results.sarif")
    
    _, result = codeQL.execute(
        source_root=source_root,
        database_path=database_path,
        results_path=results_path
    )
    
    
    
    return result