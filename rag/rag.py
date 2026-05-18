import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# ========================================
# STEP 1 — PDF TEXT EXTRACTION
# ========================================

def extract_text_from_pdf(pdf_path):
    """PDF la irundhu text extract pannudhu"""
    print(f"\nReading PDF: {pdf_path}")
    
    doc = fitz.open(pdf_path)
    text_pages = []
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        if text.strip():  # Empty page skip pannuvom
            text_pages.append({
                "content": text,
                "page": page_num + 1  # Page numbers 1 from start
            })
    
    doc.close()
    print(f"Extracted {len(text_pages)} pages")
    return text_pages


# ========================================
# STEP 2 — CHUNKING
# ========================================

def create_chunks(text_pages):
    """Pages → smaller chunks split pannudhu"""
    print("\nCreating chunks...")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # Each chunk — 500 characters
        chunk_overlap=100,     # 50 chars overlap — context loss illama
        separators=["\n\n", "\n", ".", " "]  # Split priority
    )
    
    all_chunks = []
    all_metadata = []
    
    for page_data in text_pages:
        chunks = splitter.split_text(page_data["content"])
        
        for chunk in chunks:
            all_chunks.append(chunk)
            all_metadata.append({"page": page_data["page"]})
    
    print(f"Created {len(all_chunks)} chunks")
    return all_chunks, all_metadata


# ========================================
# STEP 3 — EMBEDDINGS + VECTOR STORE
# ========================================

def create_vector_store(chunks, metadata):
    """Chunks → Embeddings → ChromaDB store pannudhu"""
    print("\nCreating embeddings and storing in ChromaDB...")
    print("This will take a few minutes...")
    
    # Embedding model — nomic-embed-text
    embeddings = OllamaEmbeddings(model="nomic-embed-text")
    
    # ChromaDB — local folder la store aagum
    vector_store = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        metadatas=metadata,
        persist_directory="./chroma_db"  # Local folder
    )
    
    print("Vector store created successfully")
    return vector_store


# ========================================
# STEP 4 — RETRIEVAL + ANSWER
# ========================================

def get_answer(question, vector_store):
    """Question → relevant chunks find → LLM answer"""
    
    # Similar chunks search pannuvom
    results = vector_store.similarity_search(
        question,
        k=3  # Top 3 most relevant chunks
    )
    
    # Context build pannuvom
    context = ""
    sources = []
    
    for i, doc in enumerate(results):
        context += f"\n[Source {i+1} - Page {doc.metadata['page']}]\n"
        context += doc.page_content
        context += "\n"
        sources.append(doc.metadata['page'])
    
    # LLM setup
    llm = ChatOllama(model="llama3:8b")
    parser = StrOutputParser()
    
    # Prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a helpful assistant that answers questions 
based on the provided document context only.

Rules:
1. Answer only from the context provided
2. Always mention which page the answer is from
3. If answer not in context, say "Not found in document"
4. Keep answers concise and clear"""),
        ("human", """Context from document:
{context}

Question: {question}

Answer based on the context above:""")
    ])
    
    chain = prompt | llm | parser
    
    answer = chain.invoke({
        "context": context,
        "question": question
    })
    
    return answer, list(set(sources))


# ========================================
# MAIN — FULL FLOW
# ========================================

def main():
    print("=" * 50)
    print("   PDF Question Answering System")
    print("   Powered by Llama3 + ChromaDB")
    print("=" * 50)
    
    # PDF path
    pdf_path = "document.pdf"
    
    # PDF exists check
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found")
        print("Please place a PDF file named 'document.pdf' in this folder")
        return
    
    # STEP 1 — Extract
    text_pages = extract_text_from_pdf(pdf_path)
    
    # STEP 2 — Chunk
    chunks, metadata = create_chunks(text_pages)
    
    # STEP 3 — Embed + Store
    vector_store = create_vector_store(chunks, metadata)
    
    print("\n" + "=" * 50)
    print("PDF indexed successfully. Ready for questions.")
    print("Type 'exit' to quit")
    print("=" * 50)
    
    # STEP 4 — QA Loop
    while True:
        question = input("\nYour Question: ").strip()
        
        if not question:
            print("Please enter a question")
            continue
            
        if question.lower() == "exit":
            print("Goodbye.")
            break
        
        print("\nSearching document...\n")
        
        answer, sources = get_answer(question, vector_store)
        
        print(f"Answer:\n{answer}")
        print(f"\nSources: Page {sources}")
        print("-" * 50)


if __name__ == "__main__":
    main()