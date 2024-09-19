
from agent.sampling import SamplingPipeline 

class SamplingPipeline:
    def __init__(self, llm, tools, augmenter, llm_type):    
        self.tokens_used = 0
        self.total_chain_invocations = 0
        self.llm_type = llm_type
        self.llm = llm
        self.augmenter = augmenter
        self.tools = tools 
        
        
        
    def predict(self, function_body):

        self.total_chain_invocations += 1
        augmented_prompt = self.augmenter.augment(function_body)
        print(augmented_prompt[0].content)
        
        
        response = self.llm.invoke(augmented_prompt)
        
        print(response.content, '\n')
        if "@@vulnerable@@" in response.content.lower():
            print('vulnerable')
            return 1
        else:
            print('not vulnerable')
            return 0 #FIXME: Code duplication
        