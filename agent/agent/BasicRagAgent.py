from agent.agent.agent import Agent
from langchain_openai import ChatOpenAI
from llm.chatgpt import ChatGPT_LLM_Chain
from sast.tools import execute_codeql
from agent.prompt_augment.basic_augment import BasicAugmenter 
from agent.rag.vector_database.initialize import ChromaVectorDatabaseInitializer
from agent.code_context.cpp import CppFunctionContextProvider
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from sast.codeql import CodeQL
from config import Config
import os
from pprint import pprint


class BasicRagAgent():
    def __init__(self):
        
        self.sast = CodeQL()
        self.llm = ChatGPT_LLM_Chain(gpt_version='gpt-3.5-turbo-0125')
        self.contextProvider = CppFunctionContextProvider()
        self.promptAugmenter = BasicAugmenter()
        self.ragEngine = ChromaVectorDatabaseInitializer(database_path = "./database", resources_path = "./resources")
        
    

    def run(self) -> str:
        
        sast_results = self.sast.execute(
            source_root = Config["source_root"],
            database_path = Config["database_path"],
            results_path = Config["results_path"]
        )
        
        
        processed_results = list()
        for sast_result in sast_results:
            
            for location in sast_result["result_info"]["locations"]:
                code_snippet = self.contextProvider.provide_context(
                    file_path = os.path.join(Config["source_root"], location["file"]),
                    start_row = location["start_line"], #TODO: Generalize naming
                    end_row = location["end_line"] #TODO: Generalize naming
                )
                

            
                processed_result = {
                    "file" : location["file"],
                    "rule" : sast_result["result_info"]["rule_id"],
                    "message" : sast_result["result_info"]["message"],
                    "code" : code_snippet,
                    "severity" : sast_result["result_info"]["severity"],
                }
                
                processed_results.append(processed_result)
        
                
        for i, processed_result in enumerate(processed_results):
            chunks = self.ragEngine.invoke(processed_result["message"])
            vulnerability_context = list()
            for chunk in chunks:
                vulnerability_context.append(chunk.page_content)
        
            vulnerability_context = "\n".join(vulnerability_context)
            processed_results[i]["vulnerability_context"] = vulnerability_context
            
        
        prompts = list()
        for result in processed_results:
            prompt = self.promptAugmenter.augment(
                code = result["code"],
                file_path = result["file"],
                code_context = result["code"],
                sast_results = result["message"],
                vulnerability_context = result["vulnerability_context"]
            )
            
            prompts.append(prompt)
        
        for prompt in prompts:
            response = self.llm.invoke(prompt)
            print(response)
            
        
        
        
        
        
        # augment(self, code : str, file_path : str, code_context : str = "", sast_results : str = "", vulnerability_context : str = "") -> List[BaseMessage]:
        
        
            
                
                
        return 
        
        
    