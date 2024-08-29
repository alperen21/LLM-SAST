
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import os

class ChromaVectorDatabaseInitializer:
    
    def __init__(self, database_path : str, resources_path : str) -> None:
        """
        Args:
            database_path (str): _description_
            resources_path (str): _description_
        """
        self.database_path = database_path
        self.resources_path = resources_path
        
        self.__initialize()
        
    def __get_pdf_paths(self, directory):
        pdf_paths = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.lower().endswith('.pdf'):
                    pdf_paths.append(os.path.join(root, file))
        return pdf_paths
        
    def __initialize(self):
        """
        Initialize the database
        """
        pdf_files = self.__get_pdf_paths(self.resources_path)
        
        documents = []
        for pdf_file in pdf_files:
            loader = PyMuPDFLoader(pdf_file)
            documents.extend(loader.load())
            
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(documents)

        embeddings = OpenAIEmbeddings()
        
        vector_db = Chroma.from_documents(chunks, embeddings, persist_directory=self.database_path)

        retriever = vector_db.as_retriever()
        self.retriever = retriever

        print(f"Vector database has been persisted at {self.database_path}")
        
        return self.retriever

    def get_retriever(self):
        """
        Get the retriever
        """
        if not os.path.exists(self.database_path):
            self.__initialize()
        vector_db = Chroma(persist_directory=self.database_path, embedding_function=OpenAIEmbeddings())
        self.retriever = vector_db.as_retriever()
        
        return self.retriever

    def invoke(self, question : str):
        """
        Args:
            question (str): _description_
        """
        return self.retriever.invoke(question)