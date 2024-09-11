from agent.self_refinement.Analysis import AnalysisAgent
from agent.self_refinement.FeedBack import FeedBackAgent
from agent.self_refinement.Decision import DecisionAgent
from langchain.agents import initialize_agent, AgentType, tool
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from langchain.callbacks import get_openai_callback
from langchain_core.messages.base import BaseMessage
from config import Config

class SelfRefiningAgents:
    """
    Pipeline that creates a ReAct agent with SAST tools introduced as LangChain tools and also a self-refine mechanism
    """
    #TODO: Change Naming to LLM2SAST to better reflect the nature of the pipeline
    def __init__(self, llm, tools, augmenter, llm_type):
        
        self.analysis_agent = AnalysisAgent(llm, llm_type)
        self.feedback_agent = FeedBackAgent(llm, llm_type, max_feedback_loop = Config["max_feedback_loop"])
        self.decision_agent = DecisionAgent(llm, llm_type, tools)
        
        self.augmenter = augmenter
    
        
    def predict(self, function_body : str) -> int:
        """
        Predicts if the given function is vulnerable or not

        Args:
            function_body (str): the function body under test

        Returns:
            int: 1 if vulnerable, 0 if not vulnerable
        """
        
        refinement_needed = True 
        
        self.analysis_agent.set_code(function_body)
        self.analysis_agent.analyze_code()  
        analysis = self.analysis_agent.get_analysis() 
        
        print(analysis)
        
        print("="*100, "\n")
        
        refinement_needed = self.feedback_agent.is_further_refinement_needed(analysis)

        print("="*100, "\n")
        
        while (refinement_needed):
            feedback = self.feedback_agent.provide_feedback(analysis)
            print("="*100, "\n")
            
            self.analysis_agent.refine(analysis, feedback)
            analysis = self.analysis_agent.get_analysis()
            
            print(analysis, "\n","="*100, "\n")
            
            refinement_needed = self.feedback_agent.is_further_refinement_needed(analysis)
        
        print("amount of given feedbacks:", self.feedback_agent.given_feedback_count)
        self.feedback_agent.reset()
        
        response = self.decision_agent.predict(function_body, analysis)
        
        return response
    
    def get_tokens_used(self):
        analysis_tokens = self.analysis_agent.get_tokens_used()
        feedback_tokens = self.feedback_agent.get_tokens_used()
        decision_tokens = self.decision_agent.get_tokens_used()
        
        
        return {
            'tokens_used' : analysis_tokens["tokens_used"] + feedback_tokens["tokens_used"] + decision_tokens["tokens_used"], 
            'total_chain_invocations' :  analysis_tokens["total_chain_invocations"] + feedback_tokens["total_chain_invocations"] + decision_tokens["total_chain_invocations"], 
            }
        
        
