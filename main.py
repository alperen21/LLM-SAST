#!/home/alp/Project/venv/bin/python
from llm.chatgpt import ChatGPT_LLM_Chain

def main():
    chain = ChatGPT_LLM_Chain()
    response = chain.invoke('hello world')

    print(response)

    response = chain.invoke('what did you say again?')

    print(response)

if __name__ == '__main__':
    main()