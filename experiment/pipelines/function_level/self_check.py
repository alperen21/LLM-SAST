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
        There might be an error in the solution above because of lack of understanding of the question. Please correct the error in your reasoning (not code), if any, and rewrite the solution.
        """

    

class SelfCheckSAST(AgentToSast):
    def __init__(self, llm, tools, augmenter, llm_type):
        super().__init__(llm, tools, augmenter, llm_type)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        # Initialize agent with memory
        self.agent = initialize_agent(
            tools=tools,  
            llm=llm,  
            agent_type=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  
            verbose=True,  
            handle_parsing_errors=True,
            memory=self.memory  
        ) 
    
    def predict(self, function_body):
        """
        Predicts if the function is vulnerable and performs self-checking of reasoning
        """

        self.total_chain_invocations += 1
        augmented_prompt = self.augmenter.augment(function_body)

        # Get response to the initial function body
        if self.llm_type == 'gpt':  # Use get_openai_callback if LLM is GPT
            with get_openai_callback() as cb:
                response = self.agent.invoke(augmented_prompt)
                self.tokens_used += cb.total_tokens

                # Now introduce the self-check prompt
                selfCheckPrompt = SelfCheckPrompt().template_string
                
                # Manually load the chat history and append it to the new prompt
                chat_history = self.memory.load_memory_variables({})["chat_history"]
                conversation_history = chat_history[0].content[0]["content"]

                # Append the conversation history to the self-check prompt
                selfCheckPrompt_with_history = selfCheckPrompt + "\n\nPrevious conversation:\n" + conversation_history
                
                # Invoke the agent again with the self-check prompt
                response = self.agent.invoke(selfCheckPrompt_with_history)
                self.tokens_used += cb.total_tokens
        else:
            response = self.agent.invoke(augmented_prompt)
        print(response)
        # Do not reset memory to preserve history between invocations
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
                # Get the LLM response to the augmented prompt
                response = self.llm.invoke(augmented_prompt)

                # Store the interaction in memory
                self.memory.chat_memory.add_user_message(function_body)
                self.memory.chat_memory.add_ai_message(response.content)
                
                # Automatically let the memory append conversation history
                selfCheckPrompt = SelfCheckPrompt().template_string
                response = self.llm.invoke(selfCheckPrompt)

                self.tokens_used += cb.total_tokens
        
        else:
            response = self.llm.invoke(augmented_prompt)

        print(response.content, '\n')

        # Avoid resetting memory after every prediction, to retain conversation history
        if "@@vulnerable@@" in response.content.lower():
            print('vulnerable')
            return 1
        else:
            print('not vulnerable')
            return 0

    def reset_memory(self):
        """
        Clears the memory, resetting the conversation history.
        """
        self.memory.clear()
        print("Memory has been reset.")