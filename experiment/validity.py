from sast.codeql import CodeQL
from config import Config
import os

class ValidityChecker:
    def check_validity(self, repo, function):
        return True 


class CodeQLValidityChecker:
    def __init__(self) -> None:
        self.codeQL = CodeQL()

    def check_if_persisted(self, line_to_append, file_path = os.path.join('validity', 'codeql_invalid.txt')):
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
        except FileNotFoundError:
            return False
        
        return line_to_append + '\n' in lines


    def persist_incompatible_repo(self, line_to_append, file_path = os.path.join('validity', 'codeql_invalid.txt')):
        with open(file_path, 'a') as file:
                file.write(line_to_append + '\n')


    def check_validity(self, repo, function=None):

        if self.check_if_persisted(repo):
            return False

        source_root = Config["test_path"]
        database_path = os.path.join(source_root, "codeql-db")
        results_path = os.path.join(source_root, "results.sarif")
        
        return_code, _ = self.codeQL.execute(
            source_root=source_root,
            database_path=database_path,
            results_path=results_path
        )

        if return_code != 0:
            self.persist_incompatible_repo(repo)
        
        return return_code == 0

