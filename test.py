from experiment.benchmarks.function_level import PrimeVulBenchmark
from config import Config
from experiment.util import RipgrepFunctionFinder
from pprint import pprint
from tqdm import tqdm

def test(total_test_case_num = 2):
    
    test_case_num = 0
    benchmark = PrimeVulBenchmark()

    
    while tqdm(test_case_num < total_test_case_num):
    
        function_body = benchmark.get_random_function()
        
        if function_body is None:
            print("No more functions to test left.")
            break

        benchmark.clean_test_directory()

        return_code = benchmark.clone_repository()
        
        if return_code != 0:
            continue

        return_code = benchmark.checkout_commit()
        
        if return_code != 0:
            continue

        # benchmark.compile_code()
        
        if return_code != 0:
            continue

        benchmark.receive_prediction(0)
        
        test_case_num += 1

    pprint(benchmark.get_results())
    
    
test()