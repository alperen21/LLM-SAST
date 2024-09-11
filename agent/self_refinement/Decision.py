

from langchain.prompts import ChatPromptTemplate
from langchain.agents import initialize_agent, AgentType
from langchain.callbacks import get_openai_callback #TODO: Code duplication! This is also present in experiment/pipelines/function_level/agent_to_sast.py

class DecisionAgent:
    def __init__(self, llm, llm_type, tools, augmenter = None): #TODO: create a class that inherits from llm and returns llm_type
        self.llm = llm
        self.augmenter = augmenter
        self.llm_type = llm_type
        self.tools = tools
        
        
        self.agent = initialize_agent(
            tools=tools,  # List of tools the agent can use
            llm=llm,  # The language model
            agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # Choose the type of agent
            verbose=True,  # Whether to print out the intermediate steps,
            handle_parsing_errors=True
        ) #TODO: LangChain's initialize_agent is now deprecated, migrate the codebase
        
        
        template_string = """
        ### Task:
        You are a security engineer lead.\n
        You have been tasked with reviewing code snippets for security vulnerabilities.\n

        ### Code: \n

        ```c
        {code}
        ```
        
        Here is the thoughts of a security engineer below you:
        ### Analysis: \n
        
        {analysis}
        
        If you are not sure, you can execute any of the tools provided to help you make a decision such as SAST tools\n
        Make note that the output of SAST tools may not always be correct.\n
        
        When you have made your decision either invoke the make_decision tool or write your decision as @@Vulnerable@@ or @@Not Vulnerable@@.\n
        """
        
        
        self.prompt_template = ChatPromptTemplate.from_template(template_string)
    
    def predict(self, function_body : str, analysis : str) -> int:
        
        prompt = self.prompt_template.format_messages(
                code = function_body,
                analysis = analysis
        )
        
        response = self.agent.invoke(prompt)

        
        if self.augmenter is not None:
            prompt = self.augmenter.augment(function_body)

        if "@@vulnerable@@" in response["output"].lower():
            print('vulnerable')
            return 1
        else:
            print('not vulnerable')
            return 0
        