from agent.prompt_augment.augment import PromptAugmenter
from langchain.prompts import ChatPromptTemplate
from typing import List
from langchain_core.messages.base import BaseMessage

class BasicAugmenter(PromptAugmenter):
    def __init__(self):
        super().__init__()
        
        template_string = """
        ### Task:
        Analyze the following code and detect any potential security vulnerabilities.
        You will also receive results from SAST tools (may not be correct all the time)
        
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
        

        Reply with the following format:\n.
            ***\n
                file_path -> file path, \n
                function_name -> function_name, \n
                decision -> @@Vulnerable@@  or @@Secure@@\n
             ***\n
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