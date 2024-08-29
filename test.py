from langchain_community.document_loaders import PyMuPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

# Step 1: Load the documents
pdf_files = [
    "agent/rag/resources/OWASP_Testing_Guide_v4-2.pdf",
    "agent/rag/resources/nistir7435.pdf"
]

documents = []
for pdf_file in pdf_files:
    loader = PyMuPDFLoader(pdf_file)
    documents.extend(loader.load())

# Step 2: Split the documents into chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)

# Step 3: Create embeddings for the chunks
embeddings = OpenAIEmbeddings()

# Step 4: Define the persistence directory
persist_directory = "./database"

# Step 5: Create the Chroma vector store and persist it
vector_db = Chroma.from_documents(chunks, embeddings, persist_directory=persist_directory)

# Step 6: Persist the database

# Step 7: Create a retriever from the Chroma vector store
retriever = vector_db.as_retriever()

print(f"Vector database has been persisted at {persist_directory}")


#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====#====
# Step 1: Define the persistence directory
persist_directory = "./database"

# Step 2: Load the persisted Chroma vector store
vector_db = Chroma(persist_directory=persist_directory, embedding_function=OpenAIEmbeddings())

# Step 3: Create a retriever from the Chroma vector store
retriever = vector_db.as_retriever()

# Step 4: Use the retriever to perform similarity search or any retrieval operation
query = "What are the common security testing practices in OWASP?"
results = retriever.invoke(query)
# for result in results:
#     print(result.page_content)