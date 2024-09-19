from langchain.prompts import ChatPromptTemplate
from agent.abstract import Agent


class DistillationAgent(Agent):
    def __init__(self, llm, llm_type, augmenter = None): #TODO: create a class that inherits from llm and returns llm_type
        super().__init__(llm_type)
        self.llm = llm
        self.augmenter = augmenter
        self.llm_type = llm_type
   
        
    def call_llm(self, prompt):
        return self.llm.invoke(prompt)

    def distill(self, prompt, code, sast_output):
        template_string = """
            ### Task:
            You are an artificial intelligence tasked to distill the given problem of deciding whether or not a code is vulnerable\n
            
            Here is the prompt and output of a sast tool create a more consise and precise analysis of the code to determine if it is vulnerable or not\n
            
            Prompt:
            {prompt}
            
            Code
            ```c
            {code}
            ```
            
            Output of the SAST tool:
            {sast_output}""" 
            
        self.prompt_template = ChatPromptTemplate.from_template(template_string)

        prompt = self.prompt_template.format_messages(
            code = code,
            prompt = prompt, 
            sast_output = sast_output
        )
        
        