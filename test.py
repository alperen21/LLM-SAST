from agent.self_refinement.Analysis import AnalysisAgent
from agent.self_refinement.FeedBack import FeedBackAgent
from agent.self_refinement.Decision import DecisionAgent
import openai
import getpass
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import pprint
from langchain.agents import initialize_agent, AgentType, tool
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from langchain_core.messages.base import BaseMessage
from util import make_decision


from sast.tools import execute_dummy_codeql

llm_analysis = ChatOpenAI(model="gpt-4o-mini", temperature = 1)
llm_feedback = ChatOpenAI(model="gpt-4o-mini", temperature = 1)
llm_decision = ChatOpenAI(model="gpt-4o-mini", temperature = 1)

benchmark_object = {"func": "cdf_check_stream_offset(const cdf_stream_t *sst, const cdf_header_t *h,\n    const void *p, size_t tail, int line)\n{\n\tconst char *b = RCAST(const char *, sst->sst_tab);\n\tconst char *e = RCAST(const char *, p) + tail;\n\tsize_t ss = cdf_check_stream(sst, h);\n\t/*LINTED*/(void)&line;\n\tif (e >= b && CAST(size_t, e - b) <= ss * sst->sst_len)\n\t\treturn 0;\n\tDPRINTF((\"%d: offset begin %p < end %p || %\" SIZE_T_FORMAT \"u\"\n\t    \" > %\" SIZE_T_FORMAT \"u [%\" SIZE_T_FORMAT \"u %\"\n\t    SIZE_T_FORMAT \"u]\\n\", line, b, e, (size_t)(e - b),\n\t    ss * sst->sst_len, ss, sst->sst_len));\n\terrno = EFTYPE;\n\treturn -1;\n}", "project": "file", "hash": 204454981683520436432921437325307670739, "size": 16, "commit_id": "46a8443f76cec4b41ec736eca396984c74664f84", "message": "Limit the number of elements in a vector (found by oss-fuzz)", "target": 0, "dataset": "other", "idx": 427706}

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
    make_decision
]

analysis_agent = AnalysisAgent(llm_analysis, 'gpt')
feedback_agent = FeedBackAgent(llm_feedback, 'gpt', max_feedback_loop = 15)
decision_agent = DecisionAgent(llm_decision, 'gpt', tools)

refinement_needed = True 
analysis_agent.set_code(benchmark_object["func"])
analysis_agent.analyze_code()
analysis = analysis_agent.get_analysis()

print(analysis)
print("="*100)
print()

refinement_needed = feedback_agent.is_further_refinement_needed(analysis)
print("="*100)
print()

while (refinement_needed):
    
    feedback = feedback_agent.provide_feedback(analysis)
    print("="*100)
    print()

    analysis_agent.refine(analysis, feedback)

    analysis = analysis_agent.get_analysis()

    print(analysis)

    print("="*100)
    print()
    
    refinement_needed = feedback_agent.is_further_refinement_needed(analysis)

print("amount of given feedbacks:", feedback_agent.given_feedback_count)


response = decision_agent.predict(benchmark_object["func"], analysis)
print(response)