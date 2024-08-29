from agent.code_context.context import ContextProvider

class BasicContextProvider(ContextProvider):
    def __init__(self) -> None:
        super().__init__()
    
    def provide_context(self, file_path: str, start_row: int = None, end_row: int = None, start_column: int = None, end_column: int = None) -> str:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            if start_row is not None and end_row is not None:
                context = ''.join(lines[start_row-1:end_row])
            else:
                context = ''.join(lines)
        return context