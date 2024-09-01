from experiment.juliet import JulietSingleExecutor
from experiment.CodeQlPipeline import CodeQlPipeline
from experiment.SingleQueryCodeQLPipeline import SingleQueryCodeQLPipeline
from config import Config
from pprint import pprint

def CodeQLExperiment():

    executor = JulietSingleExecutor()
    executor.get_labels()

    pipeline = CodeQlPipeline(Config["juliet_path"])

    executor.execute_experiment(pipeline, 1)

    pprint(executor.get_results())

def CodeQlPipelineExperiment():
    executor = JulietSingleExecutor()
    executor.get_labels()
    
    pipeline = SingleQueryCodeQLPipeline(Config["juliet_path"])
    
    pipeline.predict(None, None) #FIXME
    # executor.execute_experiment(pipeline, 0.01)
    
    # pprint(executor.get_results())

def main():
    print("executing codeql baseline experiment")
    CodeQlPipelineExperiment()
    
    
if __name__ == "__main__":
    main()
    