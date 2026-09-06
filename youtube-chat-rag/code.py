#-----------------------------------------------
#                  1. INDEXING
#-----------------------------------------------
#------------------------------------------------
#               A. DOCUMENT LOADING
#-------------------------------------------------

from dotenv import load_dotenv
load_dotenv()
from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
# Get YouTube URL from the user
youtube_url = input("Enter YouTube URL: ")

# Extract the video ID from the URL from V to & 
video_id = youtube_url.split("v=")[1].split("&")[0]

# Create YouTube Transcript API object
api = YouTubeTranscriptApi()

# Fetch the transcript using the video ID
transcript = api.fetch(video_id,languages=['en','hi'])

# Display the loaded transcript
print("Transcript:")
print(transcript)

#---------------------------------------------
#              B. CHUNKING
#---------------------------------------------

# Convert transcript into plain text
text = " ".join([snippet.text for snippet in transcript])

# Create text splitter
#chunk_size=500:Each chunk can contain approximately 500 characters.
#chunk_overlap=50:The last 50 characters of one chunk are repeated in the next chunk.

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

# Split text into chunks
chunks = text_splitter.split_text(text)

# Display chunks
print("Number of chunks:", len(chunks))

for i, chunk in enumerate(chunks[:5]):
    print(f"\nChunk {i + 1}:")
    print(chunk)

#----------------------------------------------
#                 C.EMBEDDING
#----------------------------------------------

# Create Gemini embedding model
embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

# Convert chunks into vectors
vectors = embeddings.embed_documents(chunks)

print("Number of embeddings:", len(vectors))
print("Embedding size:", len(vectors[0]))


#----------------------------------------------
#                D. VECTOR STORE
#----------------------------------------------

# Create vector store from chunks and embedding model
vector_store = FAISS.from_texts(
    chunks,
    embedding=embeddings
)

print("Vector store created successfully!")

#-------------------------------------------------------------
#                       2. RETRIEVAL
#-------------------------------------------------------------
#                      A. SEMANTIC SEARCH
#--------------------------------------------------------------

query = input("Ask a question: ")

# Search for relevant chunks
results = vector_store.similarity_search(query)


#------------------------------------------------------
#               3.AUGMENTATION
#-------------------------------------------------------

# Get the relevant chunks as text
context = "\n\n".join([result.page_content for result in results])


# Create the augmented prompt
prompt = f"""
Answer the question using only the following context.

Context:
{context}

Question:
{query}
"""


print(prompt)

#---------------------------------------------------------
#                   4. GENERATION
#---------------------------------------------------------

# Create Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)

# Generate answer
response = llm.invoke(prompt)

# Display the answer
print("\nAnswer:")
print(response.content)


