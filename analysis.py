from experiment.benchmarks.function_level import PrimeVulBenchmarkDummy
from pprint import pprint

benchmark = PrimeVulBenchmarkDummy(output_identifier='analysis')

benchmark.index = 14

data = benchmark.data


pprint(data[14])

