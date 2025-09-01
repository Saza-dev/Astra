from crewai.tools import tool

@tool("qna_tool")
def qna_tool(question: str):
    """
    Ask the user for clarification or missing information.
    
    Args:
        question (str): The clarification question to ask the user
    
    Returns:
        dict: The question to present to the user
    """
    return {"ask_user": question}
