from langchain_core.tools import tool

@tool
def make_decision(input_str) -> None: #TODO: remove and check if it changes the results
    """
    When you are ready to make decision whether or not the code snippet is vulnerable or not.
    Invoke this function to make the decision
    
    Args:
        input_str (str) : The input string to make a decision on.
        
    Returns:
        None
    """
    if "@@vulnerable@@" in input_str.lower():
        print("Vulnerable")
    else:
        print("Not Vulnerable")