from langchain_community.document_loaders import  Docx2txtLoader, PyPDFLoader, TextLoader 
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import  FAISS
import os


def ingest(pdf_path):
     # load the file 
    if pdf_path.endswith(".pdf"):
        loader = PyPDFLoader(pdf_path)
    elif pdf_path.endswith(".txt"):
        loader = TextLoader(pdf_path)
    elif pdf_path.endswith(".docx"):
        loader = Docx2txtLoader(pdf_path)   
    else :
        raise ValueError("Unsuported file type!") 
    documents = loader.load() 

    #splitiing the huge data 
    splitter = RecursiveCharacterTextSplitter(
            chunk_size = 500,
            chunk_overlap = 50
    )
    chunks = splitter.split_documents(documents)
    

    #making vectors 
    embeddings = HuggingFaceEmbeddings(
        model_name = "sentence-transformers/all-MiniLM-L6-v2"
    )


    if os.path.exists("faiss_index"):
        vectorstore = FAISS.load_local(
            "faiss_index",
            embeddings,
            allow_dangerous_deserialization=True
        )
        vectorstore.add_documents(chunks)
    else :
         vectorstore = FAISS.from_documents(chunks , embeddings)
  
    vectorstore.save_local("faiss_index") #stores a index to dirclty jump

