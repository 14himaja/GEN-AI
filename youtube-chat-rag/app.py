# -----------------------------------------------
#                  IMPORTS
# -----------------------------------------------

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, StreamingResponse

from youtube_transcript_api import YouTubeTranscriptApi
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI


# -----------------------------------------------
#                  FASTAPI APP
# -----------------------------------------------

app = FastAPI()

# Store the vector store
vector_store = None

# Create Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash"
)


# -----------------------------------------------
#                  HOME PAGE
# -----------------------------------------------

@app.get("/", response_class=HTMLResponse)
def home():

    with open("templates/home.html", "r", encoding="utf-8") as f:
        return f.read()


# -----------------------------------------------
#                  1. INDEXING
# -----------------------------------------------
#             A. DOCUMENT LOADING
# -----------------------------------------------

@app.post("/load-video", response_class=HTMLResponse)
def load_video(youtube_url: str = Form(...)):

    global vector_store

    # Extract the video ID
    video_id = youtube_url.split("v=")[1].split("&")[0]

    # Create YouTube Transcript API object
    api = YouTubeTranscriptApi()

    # Fetch transcript
    transcript = api.fetch(
        video_id,
        languages=["en", "hi"]
    )


    # -------------------------------------------
    #              B. CHUNKING
    # -------------------------------------------

    # Convert transcript into plain text
    text = " ".join(
        [snippet.text for snippet in transcript]
    )

    # Create text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    # Split text into chunks
    chunks = text_splitter.split_text(text)


    # -------------------------------------------
    #              C. EMBEDDING
    # -------------------------------------------

    # Create Gemini embedding model
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )


    # -------------------------------------------
    #              D. VECTOR STORE
    # -------------------------------------------

    # Create vector store
    vector_store = FAISS.from_texts(
        chunks,
        embedding=embeddings
    )


    # -------------------------------------------
    #              QUESTION PAGE
    # -------------------------------------------

    with open("templates/answer.html", "r", encoding="utf-8") as f:
        return f.read()


# -----------------------------------------------
#                  2. RETRIEVAL
# -----------------------------------------------
#             A. SEMANTIC SEARCH
# -----------------------------------------------

@app.post("/ask")
def ask_question(query: str = Form(...)):

    global vector_store

    # Search for relevant chunks
    results = vector_store.similarity_search(
        query,
        k=3
    )


    # -------------------------------------------
    #              3. AUGMENTATION
    # -------------------------------------------

    # Get relevant chunks as text
    context = "\n\n".join(
        [result.page_content for result in results]
    )

    # Create augmented prompt
    prompt = f"""
    Answer the question using only the following context.

    Context:
    {context}

    Question:
    {query}
    """


    # -------------------------------------------
    #              4. GENERATION
    # -------------------------------------------

    # Generate answer using streaming
    def generate_answer():

        for chunk in llm.stream(prompt):

            if isinstance(chunk.content, str):
                yield chunk.content

            elif isinstance(chunk.content, list):

                for item in chunk.content:

                    if isinstance(item, dict) and "text" in item:
                        yield item["text"]


    return StreamingResponse(
        generate_answer(),
        media_type="text/plain"
    )