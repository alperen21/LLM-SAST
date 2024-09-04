def function_level_test(pipeline, benchmark, total_test_case_num = 2):
    
    test_case_num = 0
    
    while test_case_num < total_test_case_num:
    
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
        
        if return_code != 0:
            continue

        prediction = pipeline.predict(function_body)
        benchmark.receive_prediction(prediction)
        
        test_case_num += 1

    benchmark.get_results()
    
    