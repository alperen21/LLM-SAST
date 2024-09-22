import sys
import clang.cindex

clang.cindex.Config.set_library_file('/usr/local/opt/llvm/lib/libclang.dylib')


def get_function_body(filepath, function_name):
    # Initialize the clang index
    index = clang.cindex.Index.create()

    # Parse the source file
    translation_unit = index.parse(filepath)

    # Define a recursive function to traverse the AST and find the function
    def find_function_body(node):
        # Check if the current node is a function declaration
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL and node.spelling == function_name:
            # Extract the function body as a list of tokens
            tokens = list(node.get_tokens())
            body = ''.join([t.spelling for t in tokens if t.kind == clang.cindex.TokenKind.PUNCTUATION or t.kind == clang.cindex.TokenKind.LITERAL or t.kind == clang.cindex.TokenKind.KEYWORD or t.kind == clang.cindex.TokenKind.IDENTIFIER])
            return body

        # Recurse through child nodes
        for child in node.get_children():
            result = find_function_body(child)
            if result is not None:
                return result

        return None

    # Start searching for the function body from the root of the AST
    return find_function_body(translation_unit.cursor)


print(get_function_body(sys.argv[1], sys.argv[2]))