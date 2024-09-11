from langchain.prompts import ChatPromptTemplate

class FeedBackAgent:
    def __init__(self, llm, llm_type, augmenter = None, max_feedback_loop = 5): #TODO: create a class that inherits from llm and returns llm_type
        self.llm = llm
        self.augmenter = augmenter
        self.llm_type = llm_type
        self.given_feedback_count = 0
        self.max_feedback_loop = max_feedback_loop
    
    def is_further_refinement_needed(self, analysis : str):
        
        self.given_feedback_count += 1
        
        if self.given_feedback_count >= self.max_feedback_loop:
            return False
        
        
        template_string = """
            ### Task:
            You are a security engineer manager.\n
            You will receive analysis of a code for software vulnerabilities from a security engineer.\n
            The engineer's job is to find whether or not the given code snippet is vulnerable or not \n
            The snippet may contain multiple vulnerabilities or no vulnerabilities at all\n
            You need to decide whether the analysis conveys a good understanding and is thorough or not.\n

            ### Code: \n
            
            ### Analsis: \n
            {analysis}
            
            
            
            If you think further refinement is needed because the analysis does not convey a good understanding or is not thorough enough, only reply with "yes" if you don't think so only reply with "no".
                
            """
            
        self.prompt_template = ChatPromptTemplate.from_template(template_string)
        response = self.llm.invoke(self.prompt_template.format_messages(analysis = analysis))
        
        print(response.content)
        
        return response.content.strip().lower() == "yes"

    def provide_feedback(self, analysis : str):
        
        template_string = """
            ### Task:
            You are a security engineer manager.\n
            You have been tasked with providing feedback on the analysis of a security engineer for software vulnerabilities.\n


            ### Analsis: \n
            {analysis}
            
            
            Provide feedback on the analysis.
                
            """
            
        self.prompt_template = ChatPromptTemplate.from_template(template_string)
        response = self.llm.invoke(self.prompt_template.format_messages(analysis = analysis))
        
        print(response.content)
        
        return response.content
    
    