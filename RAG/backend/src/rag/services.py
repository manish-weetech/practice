import os
import shutil
from fastapi import UploadFile
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.utils.settings import settings
import logging
import uuid
from sqlalchemy.orm import Session
from src.rag.models import DocumentModel

logger = logging.getLogger(__name__)

class RagService:
    def __init__(self):
        """Initializes the required API clients, models, and embeddings DB lazily inside the class context."""
        self.chroma_dir = "./chroma_db"
        self.temp_dir = "./temp_files"
        
        os.makedirs(self.chroma_dir, exist_ok=True)
        os.makedirs(self.temp_dir, exist_ok=True)
        
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001", 
            google_api_key=settings.GEMINI_API_KEY
        )
        self.vector_store = Chroma(
            persist_directory=self.chroma_dir, 
            embedding_function=self.embeddings
        )
        self.llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.5-flash", 
            google_api_key=settings.GEMINI_API_KEY
        )
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    async def process_document(self, file: UploadFile, db: Session, user_id: int, display_name: str = None) -> str:
        """Parses the document, chunks its content, embeds it, saves it to the vector store with a unique doc_id."""
        file_path = os.path.join(self.temp_dir, file.filename)
        doc_id = str(uuid.uuid4())
        try:
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            loader = None
            if file.filename.lower().endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file.filename.lower().endswith(".docx"):
                loader = Docx2txtLoader(file_path)
            
            if not loader:
                raise ValueError("Unsupported file type. Please upload a PDF or DOCX file.")
                
            documents = loader.load()
            chunks = self.text_splitter.split_documents(documents)
            
            # Attach doc_id to isolate documents
            for chunk in chunks:
                chunk.metadata["doc_id"] = doc_id
            
            self.vector_store.add_documents(chunks)
            
            # Persist to relational database for dashboard history
            new_doc = DocumentModel(user_id=user_id, doc_id=doc_id, filename=file.filename, display_name=display_name)
            db.add(new_doc)
            db.commit()
            db.refresh(new_doc)
            
            return doc_id
        except Exception as e:
            logger.error(f"Failed to process document: {str(e)}")
            raise e
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

    def answer_question(self, doc_id: str, question: str) -> str:
        """Retrieves relevant contexts matching doc_id from the vector db and answers the question using an LLM chain."""
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 5, "filter": {"doc_id": doc_id}})
        
        system_prompt = (
            "You are a helpful assistant for question-answering tasks. "
            "Use the following pieces of retrieved context to answer the question. "
            "If you don't know the answer, say that you don't know. "
            "Use three sentences maximum and keep the answer concise.\n\n"
            "Context:\n{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
        
        response = rag_chain.invoke({"input": question})
        return response["answer"]
