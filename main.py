from experiment.test import function_level_test
from experiment.pipelines.function_level.agent_to_sast import AgentToSast
from experiment.pipelines.function_level.llm_only import LLMOnly # type: ignore
from experiment.pipelines.function_level.sampling import SamplingPipeline, SamplingReActPipeline
from experiment.pipelines.function_level.self_refinement import SelfRefiningAgents, NoSASTSelfRefiningAgents
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from sast.tools import execute_dummy_codeql
from langchain.tools import Tool
from experiment.benchmarks.function_level import PrimeVulBenchmarkDummy
from agent.prompt_augment.basic_augment import BasicAugmenter, BasicNoToolAugmenter, CoTAugmenter, AnalogicalReasoningAugmenter, BasicAugmenterWithContext
from langchain_core.tools import tool
from experiment.validity import CodeQLValidityChecker, ValidityChecker
from state import SharedState
import sys
import code_context.tools as code_context_tools
from experiment.pipelines.function_level.self_check import SelfCheck, SelfCheckSAST

@tool
def make_decision(input_str) -> None: #TODO: remove and check if it changes the results
    """
    When you are ready to make decision whether or not the code snippet is vulnerable or not.
    Invoke this function to make the decision
    
    Args:
        input_str (str) : The input string to make a decision on.
        
    Returns:
        None
    """
    if "@@vulnerable@@" in input_str.lower():
        print("Vulnerable")
    else:
        print("Not Vulnerable")

def llm_only_experiment(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)
    validityChecker = ValidityChecker()
    
    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
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

    augmenter = BasicNoToolAugmenter()
    
    pipeline = LLMOnly(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='llm_only')
    
    function_level_test(pipeline, benchmark, validity_checker=validityChecker, total_test_case_num=total_test_case_num)


def llm_to_sast_experiment(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)
    validityChecker = ValidityChecker()

    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
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
    
    pipeline = AgentToSast(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='agent_to_sast')
    
    function_level_test(pipeline, benchmark, validity_checker = validityChecker, total_test_case_num=total_test_case_num)

def self_refine_experiment(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)
    validityChecker = ValidityChecker()
    
    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
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
    pipeline = SelfRefiningAgents(llm, tools, None, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='self_refine')
    
    function_level_test(pipeline, benchmark, validity_checker = validityChecker, total_test_case_num=total_test_case_num)

def chain_of_thought_experiment(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)
    validityChecker = ValidityChecker()

    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
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

    augmenter = CoTAugmenter()
    
    pipeline = LLMOnly(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='CoT')
    
    function_level_test(pipeline, benchmark, validity_checker = validityChecker, total_test_case_num=total_test_case_num)
    
    
def analogical_reasoning_experiment(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)
    validityChecker = ValidityChecker()

    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
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

    augmenter = AnalogicalReasoningAugmenter()
    
    pipeline = LLMOnly(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='analogical_reasoning')
    
    function_level_test(pipeline, benchmark, validity_checker = validityChecker, total_test_case_num=total_test_case_num)
#FIXME: Code Duplication


def self_refine_no_sast_experiment(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)
    validityChecker = ValidityChecker()


    augmenter = BasicNoToolAugmenter()
    
    pipeline = NoSASTSelfRefiningAgents(llm, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='self_refine_no_sast')
    
    function_level_test(pipeline, benchmark, validity_checker = validityChecker, total_test_case_num=total_test_case_num)
    

def sampling_experiment(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 1)
    validityChecker = ValidityChecker()
    
    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
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

    augmenter = BasicNoToolAugmenter()
    
    pipeline = SamplingPipeline(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='sampling_100')
    
    function_level_test(pipeline, benchmark, validity_checker=validityChecker, total_test_case_num=total_test_case_num)

def sampling_react_experiment(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 1)
    validityChecker = ValidityChecker()
    
    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
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
    
    pipeline = SamplingReActPipeline(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='sampling_100_react_')
    
    function_level_test(pipeline, benchmark, validity_checker=validityChecker, total_test_case_num=total_test_case_num)

def sampling_react_cot_experiment(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 1)
    validityChecker = ValidityChecker()
    
    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
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

    augmenter = CoTAugmenter()
    
    pipeline = SamplingReActPipeline(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='sampling_50_react_cot')
    
    function_level_test(pipeline, benchmark, validity_checker=validityChecker, total_test_case_num=total_test_case_num)

def react_sast_code_context_experiment(total_test_case_num):
    llm = ChatOpenAI(model="ft:gpt-4o-mini-2024-07-18:personal:vulnerability-small:A7yzhzZs", temperature = 0)
    validityChecker = ValidityChecker()

    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
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
    
    pipeline = AgentToSast(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='code_context')
    
    function_level_test(pipeline, benchmark, validity_checker = validityChecker, total_test_case_num=total_test_case_num, clone_repo=True)

def llm_to_sast_experiment_with_context(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o", temperature = 0)
    validityChecker = ValidityChecker()

    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
                description="Executes the static application security testing tool to detect software vulnerabilities, you don't need to use this tool if you are already ready to make a decision about the code snippet"
            )
    
    decision = Tool(
        name="make_decision",
        func=make_decision,
        description="When you are ready to make decision whether or not the code snippet is vulnerable or not. Invoke this function to make the decision"
    )
    
    tools =  code_context_tools.tools + [decision, codeql_tool]

    augmenter = BasicAugmenterWithContext()
    
    pipeline = AgentToSast(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='agent_to_sast_context4')
    
    function_level_test(pipeline, benchmark, validity_checker = validityChecker, total_test_case_num=total_test_case_num, clone_repo=True)


def selfcheck(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)
    validityChecker = ValidityChecker()

    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
                description="Executes the static application security testing tool to detect software vulnerabilities, you don't need to use this tool if you are already ready to make a decision about the code snippet"
            )
    
    decision = Tool(
        name="make_decision",
        func=make_decision,
        description="When you are ready to make decision whether or not the code snippet is vulnerable or not. Invoke this function to make the decision"
    )
    
    tools =  code_context_tools.tools + [decision, codeql_tool]

    augmenter = BasicAugmenterWithContext()
    
    pipeline = SelfCheck(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='self_check')
    
    function_level_test(pipeline, benchmark, validity_checker = validityChecker, total_test_case_num=total_test_case_num, clone_repo=True)

def selfcheck_sast(total_test_case_num):
    llm = ChatOpenAI(model="gpt-4o-mini", temperature = 0)
    validityChecker = ValidityChecker()

    codeql_tool = Tool(
                name="Execute the Static Application Security Testing",
                func=execute_dummy_codeql,
                description="Executes the static application security testing tool to detect software vulnerabilities, you don't need to use this tool if you are already ready to make a decision about the code snippet"
            )
    
    decision = Tool(
        name="make_decision",
        func=make_decision,
        description="When you are ready to make decision whether or not the code snippet is vulnerable or not. Invoke this function to make the decision"
    )
    
    tools =  code_context_tools.tools + [decision, codeql_tool]

    augmenter = BasicAugmenterWithContext()
    
    pipeline = SelfCheckSAST(llm, tools, augmenter, 'gpt')
    benchmark = PrimeVulBenchmarkDummy(output_identifier='self_check_sast')
    
    function_level_test(pipeline, benchmark, validity_checker = validityChecker, total_test_case_num=total_test_case_num, clone_repo=True)

def main():

    total_test_case_num = 100

    try:

        selfcheck(total_test_case_num)
        selfcheck_sast(total_test_case_num)
        # llm_to_sast_experiment_with_context(total_test_case_num)
        # sampling_experiment(total_test_case_num)
        # print('sampling experiment done')
        
        # llm_only_experiment(total_test_case_num)
        # print('llm only  experiment done')
        
        # analogical_reasoning_experiment(total_test_case_num)
        # print('analogical reasoning experiment done')

        # chain_of_thought_experiment(total_test_case_num)
        # print('cot experiment done')

        # llm_to_sast_experiment(total_test_case_num)
        # print('llm to sast  experiment done')

        # self_refine_experiment(total_test_case_num)
        # print('self refine experiment done')
        
        # self_refine_no_sast_experiment(total_test_case_num)
        # print('self refine no sast experiment done')
        
        # sampling_react_cot_experiment(total_test_case_num)
        
        # sampling_react_experiment(total_test_case_num)
        

    
    except Exception as e:
        state = SharedState()
        print(f'error occured with: {state.project} - {state.commit}')
        raise e

        


if __name__ == "__main__":
    main()
    
    
