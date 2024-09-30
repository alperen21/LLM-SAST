import tiktoken
import time

def estimate_tokens(text: str, model_name: str = "gpt-4",) -> int:
    """
    Counts the number of tokens in a text string for a given OpenAI model.

    Args:
        model_name (str): The name of the OpenAI model (e.g., "gpt-3.5-turbo").
        text (str): The text to tokenize.

    Returns:
        int: The number of tokens.
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # Fallback encoding if model not found
        encoding = tiktoken.get_encoding("cl100k_base")  # Common for many OpenAI models
    tokens = encoding.encode(text)
    return len(tokens)


def function_level_test(pipeline, benchmark, validity_checker, clone_repo = False, total_test_case_num = 1):
    
    test_case_num = 0
    
    while test_case_num < total_test_case_num:
    
        function_body = benchmark.get_random_function()
        

        print(function_body)
        
        if function_body is None:
            print("No more functions to test left.")
            break

        
        if clone_repo:
            
            repo_link = benchmark.get_corresponding_repo()
            
            if not validity_checker.check_validity(repo_link):
                continue

            print(repo_link)
            benchmark.clean_test_directory()
            return_code = benchmark.clone_repository()
            
            if return_code != 0:
                continue

            return_code = benchmark.checkout_commit()
            
            if return_code != 0:
                continue
            
            if return_code != 0:
                continue

        
        token = estimate_tokens(function_body)
        if token > 20000:
            continue
        
        try:
            prediction = pipeline.predict(function_body)
        except Exception:
            continue
        benchmark.receive_prediction(prediction)
        test_case_num += 1
        time.sleep(30)

    benchmark.get_results()

    return pipeline.get_tokens_used()
    

def function_level_test_token(pipeline, benchmark, validity_checker, clone_repo = False, total_test_case_num = 1):
    
    test_case_num = 0
    
    while test_case_num < total_test_case_num:
    
        function_body = benchmark.get_random_function().replace("\n", "").replace(" ", "")
        

        print(function_body)
        
        if function_body is None:
            print("No more functions to test left.")
            break

        
        if clone_repo:
            
            repo_link = benchmark.get_corresponding_repo()
            
            if not validity_checker.check_validity(repo_link):
                continue

            print(repo_link)
            benchmark.clean_test_directory()
            return_code = benchmark.clone_repository()
            
            if return_code != 0:
                continue

            return_code = benchmark.checkout_commit()
            
            if return_code != 0:
                continue
            
            if return_code != 0:
                continue

        
        token = estimate_tokens(function_body)
        if token > 20000:
            continue
        
        try:
            prediction = pipeline.predict(function_body)
        except Exception:
            continue
        benchmark.receive_prediction(prediction)
        test_case_num += 1
        time.sleep(30)

    benchmark.get_results()

    return pipeline.get_tokens_used()
    
    