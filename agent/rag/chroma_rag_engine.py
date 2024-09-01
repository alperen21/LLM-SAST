from agent.rag.vector_database.initialize import ChromaVectorDatabaseInitializer
from agent.rag.rag_engines import RagEngine

class ChromaRagEngine(RagEngine):
    
    def __init__(self, database_path : str, resources_path : str) -> None:
        """
        Args:
            database_path (str): _description_
            resources_path (str): _description_
        """
        self.database_path = database_path
        self.resources_path = resources_path
        self.vector_db = None
        self.retriever = None
        self.vector_db_initializer = ChromaVectorDatabaseInitializer(database_path, resources_path)
    
    def get_relevant_chunks(self, question: str, context: str) -> str:
        """
        Args:
            question (str): _description_
            context (str): _description_
        """
        if self.retriever is None:
            self.retriever = self.vector_db_initializer.get_retriever()
        relevant_chunks =  self.retriever.get_relevant_chunks(question, context)
        
        
        if relevant_chunks:
            return relevant_chunks[0]  # Return the top chunk (most relevant)
        else:
            return None 

