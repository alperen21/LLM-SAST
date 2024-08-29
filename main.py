#!/home/alp/Project/venv/bin/python
from llm.chatgpt import ChatGPT_LLM_Chain
from agent.prompt_augment.basic_augment import BasicAugmenter
from agent.agent.BasicRagAgent import BasicRagAgent

def main():
    BasicRagAgent().run()


if __name__ == '__main__':
    main()