# # from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
# # from langchain_text_splitters import RecursiveCharacterTextSplitter
# # from langchain_huggingface import HuggingFaceEmbeddings
# # from langchain_groq import ChatGroq
# # from langchain_community.vectorstores import Chroma
# # from langchain_core.prompts import PromptTemplate
# # from dotenv import load_dotenv




# # from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RannableLambda
# # from langchain_core.output_parsers import StrOutputParser


# # load_dotenv()
# # video_id = "7xTGNNLPyMI" # only id not full url
# # try:
# #     transcript_list = YouTubeTranscriptApi().fetch(video_id)
# #     #flatten it to plain text
# #     transcript = " ".join(snippet.text for snippet in transcript_list)
# #     # print(transcript_list) 
# # except TranscriptsDisabled:
# #     print("No captions available for this video.")
    
    
# # # Text Splitting
# # splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# # chunks = splitter.create_documents([transcript])
# # # print(chunks[11])

# # # Embedding generation and Storing in vector store
# # vector_store = Chroma.from_documents(chunks, HuggingFaceEmbeddings())

# # # Retriever
# # retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})


# # # Augumentation
# # llm = ChatGroq(model="openai/gpt-oss-20b")
# # prompt = PromptTemplate(
# #     template="""
# #     You are a helpful assistent.
# #     Answer only from the provided transcript context.
# #     If the context is insufficient, just say you don't know.
# #     {context}
# #     Question: {question}
# #     """,
# #     input_variables=['context', 'question']
    
# # )
# # question = "who made this video"
# # retrieved_docs = retriever.invoke(question)
# # context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)

# # final_prompt = prompt.invoke({"context": context_text, "question": question})
# # answer = llm.invoke(final_prompt)
# # # print(answer.content)


# # # CHAIN
# # # def format_docs(retrieved_docs):
# # #     context_text = "\n\n".join(doc.page for doc in retrieved_docs)
# # #     return context_text
# # # parallel_chain = RunnableParallel({
# # #     'context': retriever | RunnableLambda(format_docs),
# # #     'question': RunnablePassthrough()
# # # })
# # # parallel_chain.invoke('who is andrej karpathy')
# # # parser = StrOutputParser()
# # # main_chain = parallel_chain | prompt | llm | parser
# # # main_chain.invoke('can you summarize the video')


import os
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from langchain_chroma import Chroma
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# Persistent ChromaDB directory
DB_PATH = str(Path(__file__).resolve().parent.parent / "chroma_db")


# ----------------------------------
# 1. Extract YouTube Video ID
# ----------------------------------

def extract_video_id(url):

    parsed_url = urlparse(url)
    host = parsed_url.hostname or ""

    if host in ["youtube.com", "www.youtube.com", "m.youtube.com"]:

        if parsed_url.path.startswith("/shorts/"):
            return parsed_url.path.split("/")[2]

        return parse_qs(parsed_url.query).get("v", [None])[0]

    elif host == "youtu.be":
        return parsed_url.path.strip("/")

    return None


# ----------------------------------
# 2. Process YouTube Video
# ----------------------------------

def process_video(video_url):

    video_id = extract_video_id(video_url)

    if not video_id:
        raise ValueError("Invalid YouTube URL!")

    # Transcript extraction
    ytt_api = YouTubeTranscriptApi()

    transcript_list = ytt_api.fetch(
        video_id,
        languages=["hi", "en"]
    )

    transcript = " ".join(
        snippet.text for snippet in transcript_list
    )

    if not transcript.strip():
        raise ValueError("Transcript is empty!")

    # Text splitting
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.create_documents(
        [transcript],
        metadatas=[{"video_id": video_id}]
    )

    # Embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # ChromaDB
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=f"youtube_{video_id}",
        persist_directory=DB_PATH
    )

    # Retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    return retriever


# ----------------------------------
# 3. Ask Question using RAG
# ----------------------------------

def ask_question(question, retriever):

    # Retrieve relevant documents
    retrieved_docs = retriever.invoke(question)

    context_text = "\n\n".join(
        doc.page_content for doc in retrieved_docs
    )

    # LLM
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.3,
    )

    # Prompt
    prompt = PromptTemplate(
        template="""
You are a helpful YouTube video assistant.

Answer only using the provided transcript context.

If the answer is not present in the context,
say that you don't know based on this video.

Context:
{context}

Question:
{question}

Answer:
""",
        input_variables=["context", "question"]
    )

    final_prompt = prompt.format(
        context=context_text,
        question=question
    )

    response = llm.invoke(final_prompt)

    return response.content
