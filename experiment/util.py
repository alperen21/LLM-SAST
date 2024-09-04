import subprocess
import os

class RipgrepFunctionFinder:
    def __init__(self, repo_path, rg_path="rg"):
        """
        Initialize the RipgrepFunctionFinder with a repository path.
        :param repo_path: Path to the repository where C/C++ files are located.
        :param rg_path: Path to the ripgrep executable (default is 'rg' assuming it's in PATH).
        """
        self.repo_path = repo_path
        self.rg_path = rg_path

    def find_function_start(self, function_name):
        """
        Use ripgrep to search for the target function in the repository.
        :param function_name: Function name to search for.
        :return: A list of matches with file path and line numbers.
        """
        # Construct a ripgrep pattern to find the function declaration using the function name
        pattern = rf"\b{function_name}\b"
        
        try:
            # Execute ripgrep to search for the function across the repo
            result = subprocess.run(
                [self.rg_path, pattern, self.repo_path, "--glob", "*.c", "--glob", "*.cpp", "--glob", "*.h", "--glob", "*.hpp"],
                capture_output=True,
                text=True,
            )
            
            # If ripgrep finds matches, return the output
            if result.stdout:
                return result.stdout.strip().split('\n')
            else:
                print(f"No matches found for function '{function_name}'.")
                return []
        except Exception as e:
            print(f"Error while searching with ripgrep: {e}")
            return []

    def extract_function_body(self, file_path, start_line):
        """
        Extract the function body by reading the file from the start_line, tracking opening and closing braces.
        :param file_path: The file containing the function.
        :param start_line: The line number where the function starts.
        :return: The full function body as a string.
        """
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Initialize tracking of braces and capturing function body
        function_body = []
        brace_count = 0
        in_function = False

        # Start reading from the start_line to find the first `{`
        for i in range(start_line - 1, len(lines)):
            line = lines[i].strip()

            # Append the line to the function body (even before we encounter the first '{')
            function_body.append(lines[i])

            # Look for the first opening `{` after the function definition
            if '{' in line and not in_function:
                brace_count += line.count('{')
                brace_count -= line.count('}')
                in_function = True

            # If we're already tracking the function body, track all braces
            elif in_function:
                brace_count += line.count('{')
                brace_count -= line.count('}')

                # If the braces are balanced, the function body is complete
                if brace_count == 0:
                    break

        return ''.join(function_body)

    def search_function_body(self, function_name):
        """
        Search for the function body in the repository using ripgrep and extract the full function body.
        :param function_name: Function name to search for.
        :return: The function body as a string, or None if not found.
        """
        matches = self.find_function_start(function_name)
        if not matches:
            return None

        # Process each match to extract the function body
        for match in matches:
            # ripgrep output format: file_path:line_number:code
            match_parts = match.split(':', 2)
            if len(match_parts) < 2:
                continue

            file_path = match_parts[0]
            start_line = int(match_parts[1])

            # Extract the function body from the file
            function_body = self.extract_function_body(file_path, start_line)

            print(f"Found function '{function_name}' in {file_path}:\n")
            print(function_body)

            return function_body

        return None

# Example Usage
if __name__ == '__main__':
    # Path to the repository
    repo_path = "/path/to/repository"

    # Path to ripgrep (e.g., "/usr/local/bin/rg" if 'rg' is not in PATH)
    rg_path = "/usr/local/bin/rg"  # Or simply 'rg' if it's in the PATH

    # Function name to search for
    target_function = "CWE190_Integer_Overflow__int_fgets_add_34_bad"

    # Create an instance of RipgrepFunctionFinder
    finder = RipgrepFunctionFinder(repo_path, rg_path)

    # Search for the function body using ripgrep
    finder.search_function_body(target_function)