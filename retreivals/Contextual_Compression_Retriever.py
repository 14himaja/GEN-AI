# Install required packages
#!pip install langchain langchain-community langchain-openai faiss-cpu

# Import required modules
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_core.documents import Document
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

# Sample documents
documents = [
    Document(
        page_content="Regular walking for 30 minutes a day improves cardiovascular health, strengthens muscles, and can reduce stress and symptoms of depression."
    ),
    Document(
        page_content="Drinking enough water throughout the day helps maintain hydration, supports metabolism, regulates body temperature, and improves energy levels."
    ),
    Document(
        page_content="Deep sleep is important for physical recovery, memory consolidation, cellular repair, and emotional regulation."
    ),
    Document(
        page_content="Eating fruits and leafy green vegetables provides essential vitamins, minerals, fiber, and antioxidants that support overall health."
    ),
    Document(
        page_content="Mindfulness and controlled breathing exercises can reduce stress, lower cortisol levels, and improve mental clarity and emotional well-being."
    )
]

# Initialize OpenAI embeddings
embedding_model = OpenAIEmbeddings()

# Create FAISS vector store
vectorstore = FAISS.from_documents(
    documents=documents,
    embedding=embedding_model
)

# Create the base retriever
base_retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

# Initialize the LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# Create the document compressor
compressor = LLMChainExtractor.from_llm(llm)

# Create Contextual Compression Retriever
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=base_retriever
)

# Define the query
query = "How can I improve my energy levels?"

# Retrieve compressed and relevant documents
results = compression_retriever.invoke(query)

# Print results
for i, doc in enumerate(results):
    print(f"\n--- Result {i+1} ---")
    print(doc.page_content)