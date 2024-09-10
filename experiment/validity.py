from sast.codeql import CodeQL
from config import Config
import os

class ValidityChecker:
    """
    Validity Checker is a class utilized to check whether the cloned repository is valid
    "Valid" in this sense refers to the idea that the SAST tools are able to work with the cloned repository
    """
    def check_validity(self, repo : str) -> bool:
        """
        Args:
            repo (str): the directory for the repository

        Returns:
            bool: returns true if the cloned repository is valid and false if not
        """
        return True 


class CodeQLValidityChecker:
    def __init__(self) -> None:
        """
        Compiles the given repository with autobuild.sh of CodeQL to check the validity
        """
        self.codeQL = CodeQL()

    def check_if_persisted(self, repo_link : str, file_path : str = os.path.join('validity', 'codeql_invalid.txt')) -> bool:
        """
        If an experiment is conducted using CodeQL within a repository a benchmark and is found to not compile with CodeQL
        the link to the repository will be persisted in a file so that when the same benchmark with CodeQL is used the experiment may skip the repository without trial

        Args:
            repo_link (str): the link to the repository            
            file_path (str, optional): the path to the file where the repository links are persisted. Defaults to os.path.join('validity', 'codeql_invalid.txt').
        
        Returns:
            bool: True if the repository link is found in the file and therefore incompatible, False otherwise
        """
        #TODO: Use hash and repo link instead since different commits can be different of the same repository
        
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                for line in file:
                    if repo_link == line.strip():
                        return True
        return False # Return False if the file doesn't exist or the repository is not included


    def check_validity(self, repo : str) -> bool:
        """
        Checks if the repository compiles with CodeQL

        Args:
            repo (str): repository link

        Returns:
            bool : True if the the repository is compatible with autobuild.sh in CodeQL and False otherwise
        """

        if self.check_if_persisted(repo): # Return False 
            return False

        source_root = Config["test_path"] # Since all repositories are cloned to the same test path and since the test path is contained in configuration file, we use this path
        database_path = os.path.join(source_root, "codeql-db") # CodeQL generates a database of the corresponding anlaysed codebase, the directory for this is also standardized 
        results_path = os.path.join(source_root, "results.sarif") # After the database is generated it is queried to see if any (standard) queries match with the codebase
        
        return_code, _ = self.codeQL.execute( # CodeQL returns the return code of subprocess used to query the database and simplified Sarif file that includes defects #TODO: Separate those into different functions
            source_root=source_root,
            database_path=database_path,
            results_path=results_path
        )

        if return_code != 0:
            self.persist_incompatible_repo(repo) # if the runtime reaches here, it means the repository does not compile with CodeQL however it was not persisted to the txt file, so the function persists it before returning the boolean value
        
        return return_code == 0

