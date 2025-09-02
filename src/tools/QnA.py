from crewai.tools import tool

@tool("qna_tool")
def qna_tool(question: str):
    """
    Ask the user for clarification.
    
    Args:
        question (str): The clarification question to show the user.
    
    Returns:
        str: A marker string prefixed with '__QNA__:' that your runner will detect
             and handle by prompting the user outside the tool execution.
    """
    return f"__QNA__:{question}"
