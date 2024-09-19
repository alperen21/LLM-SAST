import subprocess
from config import Config
import os


class CScope:
    def __init__(self) -> None:
        path = os.path.join(Config["test_path"], "cscope.files")
        subprocess.run(
            f'find {Config["test_path"]} -name "*.c" -o -name "*.cpp" -o -name "*.h" > {path}',
            cwd=Config["test_path"],
            shell=True,
        )
        print(f'cscope -b -q -k -f {Config["test_path"]}')
        subprocess.run(
            f'cd {Config["test_path"]} && cscope -b -q -k',
            shell=True,
        )
        print(f'cscope -b -q -k -f {Config["test_path"]}')
    
    def execute(self, number, query):
        process = subprocess.run(
            f'cd {Config["test_path"]} && cscope -dL -{number} {query}',
            shell=True,
            capture_output=True,
            text=True
        )
        return process.stdout
        

