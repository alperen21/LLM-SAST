from agent.prompt_augment.augment import PromptAugmenter
from langchain.prompts import ChatPromptTemplate
from typing import List
from langchain_core.messages.base import BaseMessage

class BasicAugmenter(PromptAugmenter):
    def __init__(self):
        super().__init__()
        
        self.template_string = """
        ### Task:
        You are a security engineer.\n
        You have been tasked with reviewing the following code snippet for security vulnerabilities.\n


        ### Code: \n

        ```c
        {code}
        ```
        
        If you are not sure, you can execute any of the tools provided to help you make a decision such as SAST tools\n
        Make note that the output of SAST tools may not always be correct.\n
        
        When you have made your decision either invoke the make_decision tool or write your decision as @@Vulnerable@@ or @@Not Vulnerable@@.\n
        """
        
        
        self.prompt_template = ChatPromptTemplate.from_template(self.template_string)

    
    
    def augment(self, code : str) -> List[BaseMessage]:
        '''
        Provides the code context with snippet extraction

        Args:
            prompt       (str)               : Prompt that will be augmented

        Returns:
            string : the augmented prompt
        '''
        prompt = self.prompt_template.format_messages(
            code = code,
        )


        return prompt
    
class BasicAugmenterWithContext(PromptAugmenter):
    def __init__(self):
        super().__init__()
        
        self.template_string = """
        ### Task:
        You are a security engineer.\n
        You have been tasked with reviewing the following code snippet for security vulnerabilities.\n


        ### Code: \n

        ```c
        {code}
        ```
        
        If you are not sure, you can execute any of the tools provided to help you make a decision such as SAST tools\n
        Make note that the output of SAST tools may not always be correct. Be sure to get enough context and don't heavily rely on SAST tools\n
        You can also use the provided tools to search for more context about the function. \n
        
        
        When you have made your decision explain your reasoning and write your decision as @@Vulnerable@@ or @@Not Vulnerable@@.\n
        """
        
        
        self.prompt_template = ChatPromptTemplate.from_template(self.template_string)

    
    
    def augment(self, code : str) -> List[BaseMessage]:
        '''
        Provides the code context with snippet extraction

        Args:
            prompt       (str)               : Prompt that will be augmented

        Returns:
            string : the augmented prompt
        '''
        prompt = self.prompt_template.format_messages(
            code = code,
        )


        return prompt
    
class BasicNoToolAugmenter(PromptAugmenter):
    def __init__(self):
        super().__init__()
        
        template_string = """
        ### Task:
        You are a security engineer.\n
        You have been tasked with reviewing the following code snippet for security vulnerabilities.\n


        ### Code: \n

        ```c
        {code}
        ```

        When you have made your decision either invoke the make_decision tool or write your decision as @@Vulnerable@@ or @@Not Vulnerable@@.\n
        """
        
        
        self.prompt_template = ChatPromptTemplate.from_template(template_string)

    
    
    def augment(self, code : str) -> List[BaseMessage]:
        '''
        Provides the code context with snippet extraction

        Args:
            prompt       (str)               : Prompt that will be augmented

        Returns:
            string : the augmented prompt
        '''
        prompt = self.prompt_template.format_messages(
            code = code,
        )


        return prompt
    
    

class CoTAugmenter(PromptAugmenter): #FIXME: Code duplication
    def __init__(self):
        super().__init__()
        
        self.template_string = """
        ### Task:
        You are a security engineer.\n
        You have been tasked with reviewing the following code snippet for security vulnerabilities.\n


        ### Code: \n

        ```c
        {code}
        ```

        When you have made your decision either invoke the make_decision tool or write your decision as @@Vulnerable@@ or @@Not Vulnerable@@.\n
        
        Please think step by step to solve this problem before providing the final answer
        """
        
        
        self.prompt_template = ChatPromptTemplate.from_template(self.template_string)

    
    
    def augment(self, code : str) -> List[BaseMessage]:
        '''
        Provides the code context with snippet extraction

        Args:
            prompt       (str)               : Prompt that will be augmented

        Returns:
            string : the augmented prompt
        '''
        prompt = self.prompt_template.format_messages(
            code = code,
        )


        return prompt
    
    
    
class AnalogicalReasoningAugmenter(PromptAugmenter): #FIXME: Code duplication
    def __init__(self):
        super().__init__()
        
        self.template_string = """
        ### Task:
        You are a security engineer.\n
        You have been tasked with reviewing the following code snippet for security vulnerabilities.\n


        ### Code: \n

        ```c
        {code}
        ```

        When you have made your decision either invoke the make_decision tool or write your decision as @@Vulnerable@@ or @@Not Vulnerable@@.\n
        
        Recall a related problem and then solve this one
        """
        
        
        self.prompt_template = ChatPromptTemplate.from_template(self.template_string)

    
    
    def augment(self, code : str) -> List[BaseMessage]:
        '''
        Provides the code context with snippet extraction

        Args:
            prompt       (str)               : Prompt that will be augmented

        Returns:
            string : the augmented prompt
        '''
        prompt = self.prompt_template.format_messages(
            code = code,
        )


        return prompt


class BasicNoToolAugmenter(PromptAugmenter):
    def __init__(self):
        super().__init__()
        
        template_string = """
        ### Task:
        You are a security engineer.\n
        You have been tasked with reviewing the following code snippet for security vulnerabilities.\n


        ### Code: \n

        ```c
        {code}
        ```
        When you have made your decision either invoke the make_decision tool or write your decision as @@Vulnerable@@ or @@Not Vulnerable@@.\n
        """
        
        
        self.prompt_template = ChatPromptTemplate.from_template(template_string)

    
    
    def augment(self, code : str) -> List[BaseMessage]:
        '''
        Provides the code context with snippet extraction

        Args:
            prompt       (str)               : Prompt that will be augmented

        Returns:
            string : the augmented prompt
        '''
        prompt = self.prompt_template.format_messages(
            code = code,
        )


        return prompt