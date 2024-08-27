from sast.codeql import CodeQL


tool = CodeQL()

tool.execute(
    source_root = '/home/alp/Project/demo/',
    database_path = '/home/alp/Project_Tools/codeql_db',
    results_path = '/home/alp/Project_Tools/codeql_db/results.sarif',
)