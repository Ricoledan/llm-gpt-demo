import os
import sys
import time
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from langchain.document_loaders.unstructured import UnstructuredFileLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI

load_dotenv()

app = FastAPI()
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("OPENAI_API_KEY not found in .env file")
    sys.exit(1)

loader = UnstructuredFileLoader('./docs/document.txt')
documents = loader.load()
persist_directory = 'db'


@app.get("/")
async def welcome(request: Request):
    """Welcome endpoint."""
    return 'Welcome to the LLM-GPT Demo'


@app.post("/")
async def generate_response(request: Request):
    request_data = await request.json()
    user_input = request_data['user_input']

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    split_texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()
    vector_db = Chroma.from_documents(documents=split_texts, embeddings=embeddings, persist_directory=persist_directory)

    chat_model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)
    qa = RetrievalQA.from_chain_type(llm=chat_model, chain_type="stuff", retriever=vector_db.as_retriever())

    bot_response = qa.run(user_input)
    created_time = int(time.time())

    response_data = {
        "created": created_time,
        "model": "llm-gpt-demo-v1",
        "content": bot_response
    }

    return JSONResponse(content=response_data)
