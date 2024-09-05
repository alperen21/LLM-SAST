from experiment.test import function_level_test
from experiment.pipelines.function_level.agent_to_sast import AgentToSast
from experiment.pipelines.function_level.llm_only import LLMOnly # type: ignore
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from sast.tools import execute_codeql
from langchain.tools import Tool
from experiment.benchmarks.function_level import PrimeVulBenchmark
from agent.prompt_augment.basic_augment import BasicAugmenter, BasicNoToolAugmenter
from langchain_core.tools import tool

@tool
def make_decision(input_str) -> None:
    """
    When you are ready to make decision whether or not the code snippet is vulnerable or not.
    Invoke this function to make the decision
    
    Args:
        input_str (str) : The input string to make a decision on.
        
    Returns:
        None
    """
    if "vulnerable" in input_str.lower():
        print("Vulnerable")
    else:
        print("Not Vulnerable")


def main():
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)
    
    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_codeql,
                description="Executes the static application security testing tool to detect software vulnerabilities, you don't need to use this tool if you are already ready to make a decision about the code snippet"
            )
    
    decision = Tool(
        name="make_decision",
        func=make_decision,
        description="When you are ready to make decision whether or not the code snippet is vulnerable or not. Invoke this function to make the decision"
    )
    
    tools = [
        codeql_tool,
        decision
    ]

    augmenter = BasicAugmenter()
    
    pipeline = LLMOnly(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmark(output_identifier='llm_only')
    
    function_level_test(pipeline, benchmark)

if __name__ == "__main__":
    main()
    
    
