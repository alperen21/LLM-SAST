import os
import json


class DatasetGenerator:

    def __init__(self, llm, labeled_dataset, output_dir, augmenter) -> None:
        self.llm = llm
        self.labeled_dataset = labeled_dataset
        self.output_dir = output_dir
        self.augmenter = augmenter

        # Ensure output directory exists
        os.makedirs(self.output_dir, exist_ok=True)
        self.output_file = os.path.join(self.output_dir, "finetune.jsonl")

    def generate(self):
        for func, label in self.labeled_dataset.get_next():
            prompt = self.augmenter.augment(func)
            response = self.llm.invoke(prompt)


            prediction = 1 if "@@vulnerable@@" in response.content.lower() else 0
            print('vulnerable' if prediction == 1 else 'not vulnerable')

            # If prediction matches the actual label, save to the file
            print(response)
            
            if prediction == label:
                json_obj = {
                    "function": func,
                    "label": label,
                    "response": response.content
                }

                # Append to the JSON lines file
                with open(self.output_file, 'a') as file:
                    file.write(json.dumps(json_obj) + '\n')

        print('done')