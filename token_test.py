from experiment.test import function_level_test
from experiment.pipelines.function_level.agent_to_sast import AgentToSast
from experiment.pipelines.function_level.llm_only import LLMOnly  # type: ignore
from experiment.pipelines.function_level.sampling import SamplingPipeline, SamplingReActPipeline
from experiment.pipelines.function_level.self_refinement import SelfRefiningAgents, NoSASTSelfRefiningAgents
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain_mistralai import ChatMistralAI
from sast.tools import execute_dummy_codeql
from langchain.tools import Tool
from experiment.benchmarks.function_level import CVEFixBenchmark
from agent.prompt_augment.basic_augment import (
    BasicAugmenter,
    BasicNoToolAugmenter,
    CoTAugmenter,
    AnalogicalReasoningAugmenter,
    BasicAugmenterWithContext,
)
from langchain_core.tools import tool
from experiment.validity import CodeQLValidityChecker, ValidityChecker
from state import SharedState
import sys
import code_context.tools as code_context_tools
from experiment.pipelines.function_level.self_check import SelfCheck, SelfCheckSAST


@tool
def make_decision(input_str) -> None:  # TODO: remove and check if it changes the results
    """
    When you are ready to make a decision whether or not the code snippet is vulnerable or not.
    Invoke this function to make the decision

    Args:
        input_str (str): The input string to make a decision on.

    Returns:
        None
    """
    if "@@vulnerable@@" in input_str.lower():
        print("Vulnerable")
    else:
        print("Not Vulnerable")


def get_model_identifier(llm):
    if hasattr(llm, 'model_name'):
        model_name = llm.model_name.replace(":", "_").replace("-", "_")
    else:
        model_name = "unknown_model"
    if isinstance(llm, ChatOpenAI):
        return "gpt"
    elif isinstance(llm, ChatOllama):
        return f"ollama_{model_name}"
    # elif isinstance(llm, ChatGoogleGenerativeAI):
    #     return f"google_genai_{model_name}"
    elif isinstance(llm, ChatMistralAI):
        return f"mistralai_{model_name}"
    else:
        return "unknown_model"


def llm_only_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = [codeql_tool, decision]

    augmenter = BasicNoToolAugmenter()

    pipeline = LLMOnly(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"llm_only_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"llm_only_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def llm_to_sast_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = [codeql_tool, decision]

    augmenter = BasicAugmenter()

    pipeline = AgentToSast(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"agent_to_sast_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"agent_to_sast_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def self_refine_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = [codeql_tool, decision]

    pipeline = SelfRefiningAgents(llm, tools, None, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"self_refine_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"self_refine_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def chain_of_thought_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = [codeql_tool, decision]

    augmenter = CoTAugmenter()

    pipeline = LLMOnly(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"CoT_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"CoT_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def analogical_reasoning_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = [codeql_tool, decision]

    augmenter = AnalogicalReasoningAugmenter()

    pipeline = LLMOnly(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"analogical_reasoning_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"analogical_reasoning_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def self_refine_no_sast_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    augmenter = BasicNoToolAugmenter()

    pipeline = NoSASTSelfRefiningAgents(llm, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"self_refine_no_sast_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"self_refine_no_sast_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def sampling_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = [codeql_tool, decision]

    augmenter = BasicNoToolAugmenter()

    pipeline = SamplingPipeline(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"sampling_100_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"sampling_100_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def sampling_react_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = [decision]

    augmenter = BasicAugmenter()

    pipeline = SamplingReActPipeline(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"sampling_100_react_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"sampling_100_react_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def sampling_react_cot_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = [codeql_tool, decision]

    augmenter = CoTAugmenter()

    pipeline = SamplingReActPipeline(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"sampling_50_react_cot_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"sampling_50_react_cot_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def react_code_context_experiment(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = code_context_tools.tools + [decision,]

    augmenter = BasicAugmenter()

    pipeline = AgentToSast(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"code_context_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
        clone_repo=False
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"code_context_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def llm_to_sast_experiment_with_context(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = code_context_tools.tools + [decision, codeql_tool]

    augmenter = BasicAugmenterWithContext()

    pipeline = AgentToSast(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"agent_to_sast_context_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
        clone_repo=False
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"agent_to_sast_context_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def selfcheck(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = code_context_tools.tools + [decision, codeql_tool]

    augmenter = BasicAugmenterWithContext()

    pipeline = SelfCheck(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"self_check_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
        clone_repo=False
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"self_check_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def selfcheck_sast(total_test_case_num, llm, language):
    validityChecker = ValidityChecker()
    model_id = get_model_identifier(llm)

    codeql_tool = Tool(
        name="Execute the Static Application Security Testing",
        func=execute_dummy_codeql,
        description=(
            "Executes the static application security testing tool to detect software vulnerabilities, "
            "you don't need to use this tool if you are already ready to make a decision about the code snippet"
        ),
    )

    decision = Tool(
        name="make_decision",
        func=make_decision,
        description=(
            "When you are ready to make a decision whether or not the code snippet is vulnerable or not. "
            "Invoke this function to make the decision"
        ),
    )

    tools = code_context_tools.tools + [decision, codeql_tool]

    augmenter = BasicAugmenterWithContext()

    pipeline = SelfCheckSAST(llm, tools, augmenter, model_id)
    benchmark = CVEFixBenchmark(output_identifier=f"self_check_sast_{model_id}", language=language)

    tokens = function_level_test(
        pipeline,
        benchmark,
        validity_checker=validityChecker,
        total_test_case_num=total_test_case_num,
        clone_repo=False
    )

    # Add code to write experiment name and tokens to file
    experiment_name = f"self_check_sast_{model_id}"
    with open(f"{experiment_name}.txt", "a") as f:
        f.write(experiment_name + "\n")
        f.write(str(tokens) + "\n")


def main():

    total_test_case_num = float("inf")

    languages = ['cpp', "go", "java", "js", "py", "php", "rb", "rs"]

    # Define LLM instances with desired models and temperatures
    llms = [
        ChatOpenAI(model="gpt-4o-mini", temperature=0),
        # ChatOllama(model="llama3.1", temperature=0),
        # ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0),
        # ChatMistralAI(model="codestral-latest", temperature=0),
    ]

    # List of experiment functions
    experiments = [
        # selfcheck,
        # sampling_experiment,
        llm_only_experiment,
        # analogical_reasoning_experiment,
        # chain_of_thought_experiment,
        # # llm_to_sast_experiment,
        # # self_refine_experiment,
        # self_refine_no_sast_experiment,
        # react_code_context_experiment,
        # sampling_react_cot_experiment,
        # sampling_react_experiment,
    ]

    try:
        for language in languages:
            print(f"\n=== Running experiments for Language: {language.upper()} ===\n")
            for llm in llms:
                model_id = get_model_identifier(llm)
                print(f"\nRunning experiments with LLM: {model_id}, temperature={llm.temperature}, language={language}\n")
                for experiment_func in experiments:
                    experiment_name = experiment_func.__name__
                    print(f"Starting experiment: {experiment_name} with LLM: {model_id} and Language: {language}")
                    experiment_func(total_test_case_num, llm, language)
                    print(f"Experiment {experiment_name} with LLM {model_id} and Language {language} done\n")
    except Exception as e:
        state = SharedState()
        print(f"Error occurred with: {state.project} - {state.commit}")
        raise e


if __name__ == "__main__":
    main()