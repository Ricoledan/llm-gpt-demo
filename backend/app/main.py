import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request
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
async def read_root(request: Request):
    return 'welcome to the llm-chat-gpt-demo'


@app.post("/")
async def read_root(request: Request):
    body = await request.json()
    query = body['user_input']

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    embeddings = OpenAIEmbeddings()

    vector_db = Chroma.from_documents(documents=texts, embeddings=embeddings, persist_directory=persist_directory)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vector_db.as_retriever())

    return qa.run(query)
