from langchain.prompts import ChatPromptTemplate

class AnalysisAgent: #TODO: Create an abstract agent class that returns used tokens and total chain invocations
    def __init__(self, llm, llm_type, augmenter = None): #TODO: create a class that inherits from llm and returns llm_type
        self.llm = llm
        self.augmenter = augmenter
        self.llm_type = llm_type
        self.code = None
        self.analysis = None 
        self.no_followup_action = "Do not provide any Follow-Up Actions and only analyse the code and don't make any suggestions, you only need to analyse the code to see if it is vulnerable or not"
    
    def set_code(self, code):
        self.code = code
        
    def __set_analysis(self, analysis):
        print(analysis)
        self.analysis = analysis

    def analyze_code(self):
        
        if self.code is None:
            raise ValueError("Code is not set")
        
        prompt = None
        if self.augmenter is not None:
            prompt = self.augmenter.augment(self.code)
        else:
            template_string = """
                ### Task:
                You are a security engineer.\n
                You have been tasked with reviewing the following code snippet for security vulnerabilities.\n


                ### Code: \n

                ```c
                {code}
                ```
                
                Make an argument why the code is vulnerable or not vulnerable.\n
                Do not talk about hypothetical scenarios or what the code could do. \n
                Only talk about whether or not the code snippet is vulnerable or not, not that it "could be" vulnerable or not.\n
                """ + self.no_followup_action
                
            self.prompt_template = ChatPromptTemplate.from_template(template_string)

            prompt = self.prompt_template.format_messages(
                code = self.code,
            )
        
        response = self.llm.invoke(prompt)
        self.__set_analysis(response.content)
    
    def get_analysis(self):
        return f"""
        Here is the code and the analysis the cyber security expert has made: \n\n
        Code: {self.code} \n
        Analysis : {self.analysis} \n
        """
    
    def refine(self, analysis, feedback):
        
        template_string = """
            ### Task:
            You are a security engineer.\n
            You have been tasked with refining the analysis of a code for software vulnerabilities.\n
            You had made the following analysis: \n

            ### Analsis: \n
            {analysis}
            
            Your manager provided the following feedback: \n
            ### Feedback: \n
            {feedback}
            
            Refine the analysis based on the feedback. \n
            """ + self.no_followup_action
            
        self.prompt_template = ChatPromptTemplate.from_template(template_string)
        response = self.llm.invoke(self.prompt_template.format_messages(analysis = analysis, feedback = feedback))
        
        self.__set_analysis(response.content)
        
        return self.analysis