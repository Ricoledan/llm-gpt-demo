# LLM-GPT-Demo

Companion piece to [Building Context-aware Question-Answering Systems with LLMs](https://medium.com/@ricoledan/building-context-aware-question-answering-systems-with-llms-b6f2b6e387ec), a step-by-step guide to using embeddings, vector search, and prompt engineering for building
context-aware question-answering systems tailored to provide quick and accurate information retrieval from your data
sources for enabling efficient and effective natural language processing applications.

## Prerequisites 

Install dependencies

`cd backend/`  
`pip install -r requirements.txt`

`cd frontend/`  
`npm i`

## Run Application

Run the backend api

`cd backend/`
` uvicorn --app-dir=./app main:app --reload`

Run the frontend application

`cd frontend/`
`npm run dev`

Best if you run them in separate terminals

