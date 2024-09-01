from experiment.pipeline import Pipeline
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
import random
from pprint import pprint


class SingleQueryCodeQLPipeline(Pipeline):
    
    def __init__(self, repository_path) -> None:
        super().__init__(repository_path)
        
        self.codeql = CodeQL()
        self.llm = ChatGPT_LLM_Chain(gpt_version='gpt-4o-mini')
        self.contextProvider = CppFunctionContextProvider()
        self.promptAugmenter = BasicAugmenter()
        self.ragEngine = ChromaVectorDatabaseInitializer(database_path = "./database", resources_path = "./resources")
        
        sast_results = self.codeql.execute(
            source_root = repository_path, #TODO: Generalize naming
            results_path = os.path.join(repository_path,'results.sarif'),
            database_path = Config["database_path"] 
        )
        
        
        results = list()
        for sast_result in sast_results:
            
            for location in sast_result["result_info"]["locations"]:
                code_snippet = self.contextProvider.provide_context(
                    file_path = os.path.join(repository_path, location["file"]),
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
                
                results.append(processed_result)
                
        for i, processed_result in enumerate(results):
            chunks = self.ragEngine.invoke(processed_result["message"])
            vulnerability_context = list()
            for chunk in chunks:
                vulnerability_context.append(chunk.page_content)
        
            vulnerability_context = "\n".join(vulnerability_context)
            results[i]["vulnerability_context"] = None  #TODO: Removed RAG for now due to OpenAI vulnerability_context
            
        self.prompts = list()
        for result in results:
            prompt = self.promptAugmenter.augment(
                code = result["code"],
                file_path = result["file"],
                code_context = result["code"],
                sast_results = result["message"],
                vulnerability_context = result["vulnerability_context"]
            )
            

            self.prompts.append(prompt)

    
    def predict(self, file_path, function): #TODO: more intiutive naming
        # sampled_prompts = random.sample(self.prompts, 30)
        
        
        
        vulnerable = list()
        not_vulnerable = list()
        for prompt in self.prompts:
            response = self.llm.invoke(prompt)
            
            response = response.split("***")[1].split("\n")
            response = [elem for elem in response if elem != '']
            
            file_info, function_info, decision_info = response
            
            _, file = file_info.split("->")
            _, function = function_info.split("->")
            _, decision = decision_info.split("->")
            
            decision = decision.strip()
            
            if decision == "@@Vulnerable@@":
                vulnerable.append(function)
            else:
                not_vulnerable.append(function)
                
        print(f"Vulnerable functions")
        
        for vuln in vulnerable:
            print(vuln)
            
        print(f"Not Vulnerable functions")
        
        for nvuln in not_vulnerable:
            print(nvuln)
                
            
        
            
        