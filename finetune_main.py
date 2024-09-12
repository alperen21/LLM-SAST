from finetune.finetune_dataset_generation import DatasetGenerator
from langchain_ollama import ChatOllama
from finetune.labeled_dataset import PrimeVul
from agent.prompt_augment.basic_augment import BasicNoToolAugmenter


def main():

    llm = ChatOllama(model="llama3.1", temperature = 0)
    primeVulDataset = PrimeVul()
    augmenter = BasicNoToolAugmenter()

    datasetGenerator = DatasetGenerator(
        llm = llm, 
        labeled_dataset = primeVulDataset,
        output_dir = 'finetune_dataset',
        augmenter = augmenter
    )

    datasetGenerator.generate()


if __name__ == '__main__':
    main()