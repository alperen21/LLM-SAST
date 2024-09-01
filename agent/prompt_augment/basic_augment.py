from agent.prompt_augment.augment import PromptAugmenter
from langchain.prompts import ChatPromptTemplate
from typing import List
from langchain_core.messages.base import BaseMessage

class BasicAugmenter(PromptAugmenter):
    def __init__(self):
        super().__init__()
        
        template_string = """
        ### Task:
        You are a cybersecurity expert and code auditor. 
        Your task is to analyze the following code and detect any potential security vulnerabilities.
        Focus on common security issues such as:
        injection attacks, buffer overflows, insecure data handling, authentication flaws, and improper access controls.
        You will also receive results from a static analysis tool to help you identify potential vulnerabilities, 
        note that SAST tool may not be correct all the time.
        If there is any further code context it will be given to you under '### Code Context:'
        If there is any further vulnerability context it will be given to you under '### Vulnerability Context:'
        
        
        ### File:
        {file_path}
        
        ### Code:
        {code}
        
        ### Code Context:
        {code_context}
        
        ### SAST Results:
        {sast_results}
        
        ### Vulnerability Context:
        {vulnerability_context}
        

        ### Requirements:
        1. **Identify Vulnerabilities**: Analyze the code and identify any potential security vulnerabilities.
        2. **Reply**: Reply with @@Vulnerable@@ if you find any vulnerabilities, or @@Secure@@ if you don't.
        """
        
        
        self.prompt_template = ChatPromptTemplate.from_template(template_string)

    
    
    def augment(self, code : str, file_path : str, code_context : str = "", sast_results : str = "", vulnerability_context : str = "") -> List[BaseMessage]:
        '''
        Provides the code context with snippet extraction

        Args:
            prompt       (str)               : Prompt that will be augmented

        Returns:
            string : the augmented prompt
        '''
        prompt = self.prompt_template.format_messages(
            file_path = file_path,
            code = code,
            code_context = code_context,
            sast_results = sast_results,
            vulnerability_context = vulnerability_context
        )


        return prompt