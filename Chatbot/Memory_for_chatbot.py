from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
#Load raw PDFs:

DATA_PATH="Data/"
   #This function would return the pages of the pdfs
def load_pdf_files(data):
    loader=DirectoryLoader(data,glob='*.pdf',loader_cls=PyPDFLoader)
    documents=loader.load()
    return documents
documents= load_pdf_files(DATA_PATH)

#Create Chunks of the data:

def create_chunks(extracted_data):
    splitter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
    text_chunks=splitter.split_documents(extracted_data)
    return text_chunks
text_chunks=create_chunks(documents)

# Choose Embedding Model from Hugging Face
def the_embedding_model():
    embedding_model=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return embedding_model
embedding_model=the_embedding_model()

#Make Vector database and make embeddings of the text chunk

DB_file_path="vectorstore/db_faiss"
db=FAISS.from_documents(text_chunks,embedding_model)
db.save_local(DB_file_path)