from experiment.pipelines.function_level.agent_to_sast import AgentToSast
from experiment.pipelines.function_level.llm_only import LLMOnly 
from langchain.callbacks import get_openai_callback
from langchain.prompts import ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, AgentType, tool

class SelfCheckPrompt:
    def __init__(self):
        super().__init__()
        
        self.template_string = """
        Do you think your answer was incorrect? Explain your reasoning and then reply with @@Vulnerable@@ or @@Not Vulnerable@@ again
        """

    

class SelfCheckSAST(AgentToSast):
    def __init__(self, llm, tools, augmenter, llm_type):
        super().__init__(llm, tools, augmenter, llm_type)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.agent = initialize_agent(
            tools=tools,  # List of tools the agent can use
            llm=llm,  # The language model
            agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # Type of agent
            verbose=True,  # Print out intermediate steps
            handle_parsing_errors=True,
            memory=self.memory  # Adding memory to the agent
        ) 
    def predict(self, function_body):
        self.total_chain_invocations += 1

        augmented_prompt = self.augmenter.augment(function_body)

        if self.llm_type == 'gpt': #use get_openai_callback if the used llm type is gpt
            with get_openai_callback() as cb:
                response = self.agent.invoke(augmented_prompt)
                selfCheckPrompt = SelfCheckPrompt()
                
                response = self.agent.invoke(selfCheckPrompt.template_string)

                self.tokens_used += cb.total_tokens
        
        else:
            response = self.agent.invoke(augmented_prompt)


        if "@@vulnerable@@" in response["output"].lower():
            print('vulnerable')
            return 1
        else:
            print('not vulnerable')
            return 0
        


    
class SelfCheck(LLMOnly):
    def __init__(self, llm, tools, augmenter, llm_type):
        super().__init__(llm, tools, augmenter, llm_type)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        
    def predict(self, function_body):

        self.total_chain_invocations += 1

        augmented_prompt = self.augmenter.augment(function_body)

        print(augmented_prompt[0].content)

        if self.llm_type == 'gpt':
            with get_openai_callback() as cb:
                response = self.llm.invoke(augmented_prompt)
                
                self.memory.chat_memory.add_user_message(function_body)
                self.memory.chat_memory.add_ai_message(response.content)
                
                chat_history = self.memory.load_memory_variables({})["chat_history"]
                conversation_history = "\n".join([msg.content for msg in chat_history])

                selfCheckPrompt = SelfCheckPrompt().template_string + "\n" + conversation_history
                response = self.llm.invoke(selfCheckPrompt)

                self.tokens_used += cb.total_tokens
        
        else:
            response = self.llm.invoke(augmented_prompt)

        print(response.content, '\n')
        if "@@vulnerable@@" in response.content.lower():
            print('vulnerable')
            return 1
        else:
            print('not vulnerable')
            return 0
    
