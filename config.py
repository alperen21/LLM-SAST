import os

# Specify the directory containing the .sarif files
directory = './codeql_results'
hash_codes = []
# Iterate through all files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.sarif'):
        # Extract the hash code between _ and .sarif
        hash_code = filename.split('_')[-1].split('.sarif')[0]
        hash_codes.append(hash_code)        
        hash_codes
    
Config = {
    "source_root" :"./demo",
    "database_path" : "/home/alp/Project/LLM-SAST-Benchmark/test/codeql-db",
    "results_path" : "/home/alp/Project/LLM-SAST-Benchmark/testresults.sarif",
    "juliet_path" : "/Users/alperen/Downloads/C/testcases__/CWE190_Integer_Overflow/s02/",
    "primevul_path" : "/home/alp/Desktop/LLM-SAST-Benchmark/PrimeVul_Data/",
    "test_path" : "/home/alp/Project/LLM-SAST-Benchmark/test",
    "dummy_codeql_results": "./codeql_results",
    "dummy_codeql_commits" : hash_codes,
    "max_feedback_loop" : 5
}


