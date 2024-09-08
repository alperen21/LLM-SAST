from sast.codeql import CodeQL
from config import Config
import os

class CodeQLPipeline:
    def __init__(self) -> None:
        self.codeQL = CodeQL()
        self.scan()

    
    def scan(self):
        source_root = Config["test_path"]
        database_path = os.path.join(source_root, "codeql-db")
        results_path = os.path.join(source_root, "results.sarif")
        
        self.result = self.codeQL.execute(
            source_root=source_root,
            database_path=database_path,
            results_path=results_path
        )
        
        return self.result
    
    
 