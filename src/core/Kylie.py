from dotenv import load_dotenv
from crewai import Task, Crew

load_dotenv()

def Kylie(q):
    """
    Main function to handle user queries with file operations
    """
    
    # Import agents 
    from src.agents.file_operations import file_agent
    from src.agents.question_answers import qa_agent

    
    # Determine if the query is file-related
    is_file_query = any(keyword in q.lower() for keyword in ['open', 'file', 'search', 'find', 'launch', 'start'])
    
    if is_file_query:
        # File-related query
        file_task = Task(
            description=f"Process this file request: {q}\nSearch for matching files and open the most relevant one.",
            expected_output="Confirmation of file opened with path, or error message if not found",
            agent=file_agent
        )
        
        crew = Crew(
            agents=[file_agent],
            tasks=[file_task],
        )
        
        result = crew.kickoff()


    else:
        # General Q&A
        qa_task = Task(
            description=f"Answer this question: {q}",
            expected_output="A clear and concise answer addressing the user's question",
            agent=qa_agent
        )
        
        crew = Crew(
            agents=[qa_agent],
            tasks=[qa_task],
        )
        
        result = crew.kickoff()
    
    return str(result)
