import os
import streamlit as st
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings

def load_faiss_index(file_path):
    index_dir = os.path.join(os.getcwd(), "Z_Records")
    os.makedirs(index_dir, exist_ok=True)
    index_path = os.path.join(index_dir, f"faiss_index_{os.path.basename(file_path)}")

    print("loading embedding model...")
    embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    db = get_document_embed_db(file_path, embeddings)

    if db is not None:
        db.save_local(index_path)

    return db

def get_document_embed_db(file_path, _embeddings) -> FAISS:
    try:
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function = len)
        file_loader = TextLoader(file_path)
        document = file_loader.load()
        docs = splitter.split_documents(document)
        embed_model_db = FAISS.from_documents(docs, _embeddings)
        return embed_model_db
    
    except Exception as e:
        st.exception(e)
        return None
    
def get_document_embed_db_test(document, _embeddings) -> FAISS:
    try:
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50, length_function = len)
        docs = splitter.split_documents(document)
        embed_model_db = FAISS.from_documents(docs, _embeddings)
        return embed_model_db
    
    except Exception as e:
        st.exception(e)
        return None
    