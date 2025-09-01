from dotenv import load_dotenv
from crewai import Task, Crew
from core.history import add_to_history, conversation_history

load_dotenv()

def Kylie(q):
    """
    Main function to handle user queries with file operations
    """
    
    # Import agents 
    from src.agents.file_operations import file_agent
    from src.agents.question_answers import qa_agent
    from src.agents.os_operations import os_agent

    
    # Combine history into a prompt string
    history_prompt = "\n".join([f"{h['role']}: {h['content']}" for h in conversation_history])

    
    # Determine if the query is file-related
    is_file_query = any(keyword in q.lower() for keyword in ['open', 'file', 'search', 'find', 'launch', 'start','close','create','delete','list'])
    is_os_query = any(keyword in q.lower() for keyword in ['connect', 'wifi', 'networks', 'bluetooth', 'disconnect'])
    
    if is_file_query:
        # File-related query
        file_task = Task(
            description=f"Process the file request: {q}\n Do the user requested file operations according to your knowledge",
            expected_output="Confirmation of the completed file operation, or error message",
            agent=file_agent
        )
        
        crew = Crew(
            agents=[file_agent],
            tasks=[file_task],
            verbose=True
        )
        
        result = crew.kickoff()

    elif is_os_query:
        # Os related query
        os_task = Task(
            description=f"Process the os request: {q}\n Do the user requested os operations according to your knowledge and you must use a given tool.",
            expected_output="Confirmation of the completed os operation, or error message",
            agent=os_agent
        )
        
        crew = Crew(
            agents=[os_agent],
            tasks=[os_task],
            verbose=True
        )
        
        result = crew.kickoff()

    else:
        # Add user input to history
        add_to_history("user", q)
        
        # General Q&A
        qa_task = Task(
            description=f"{history_prompt}\n\nAnswer this question: {q}",
            expected_output="A clear and concise answer addressing the user's question",
            agent=qa_agent
        )
        
        crew = Crew(
            agents=[qa_agent],
            tasks=[qa_task],
            verbose=True
        )
        
        result = crew.kickoff()
    
        add_to_history("agent", str(result))

    return str(result)
