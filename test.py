from experiment.juliet import JulietSingleExecutor
from pprint import pprint
from experiment.CodeQlPipeline import CodeQlPipeline
from config import Config
import sys



executor = JulietSingleExecutor()
executor.get_labels()

pprint(executor.labels)


pipeline = CodeQlPipeline(Config["juliet_path"])

executor.execute_experiment(pipeline, 1)

pprint(executor.get_results())