from langchain_groq import ChatGroq
from pathlib import path 
from langchain_text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
text_files =["file1.txt", "file2.txt", "file3.txt"]
documents = []
for file_path in text_files:
    loader = TextLoader(str(file_path), encoding="utf-8")
    documents.extend(loader.load())
print(f"Number of documents loaded: {len(documents)}")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
chunks = text_splitter.split_documents(documents)
print(f"Number of chunks: {len(chunks)}")
embeddings = OllamaEmbeddings(model="text-embedding-3-small")
vectordb = FAISS.from_documents(chunks, embeddings)
mypath= path("my_faiss_index")

import os 
os.makedirs(mypath, exist_ok=True)
vectordb.save_local(str(mypath))  
os.environ['GROQ_API_KEY'] = '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'
llm = ChatGroq(model="qwen/qwen3-32b", temperature=0.7, max_tokens=2000)

#for company policy retrieval in hr agent 