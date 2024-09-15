import os
import json
from config import Config


class Dataset:
    def get_next(self):
        raise NotImplementedError

class PrimeVul(Dataset):
    def __init__(self) -> None:
        super().__init__()
        
        primevul_path = Config['primevul_path']
        self.benchmark_path = os.path.join(primevul_path, 'primevul_test.jsonl')

    def get_next(self):
        with open(self.benchmark_path, 'r') as file:
            for line in file:
                training_example = json.loads(line)

                function_body = training_example['func']
                label = training_example['target']

                yield (function_body, label)

