from flask import Flask, render_template, jsonify , request
import os
from src.helper import download_embedding
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt


app=Flask(__name__)

load_dotenv()
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

embeddings=download_embedding()
index_name="medical-chatbot"

from langchain_pinecone import PineconeVectorStore
doc_search=PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)

retriever=doc_search.as_retriever(search_type="similarity", search_kwargs={"k":3})

prompt= ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}"),
    ]
)

llm=ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    max_retries=2,
    timeout=None,
    max_tokens=None
)

rag_chain=(
    {"context": lambda x: retriever.invoke(x["input"]), 
     "input": lambda x: x["input"]
    }
    | prompt
    | llm
)



@app.route("/")
def index():
    return render_template("chatbot.html")

@app.route("/get", methods=["GET","POST"])
def chat():
    data= request.get_json()
    input=data.get("message","")
    print(input)
    response=rag_chain.invoke({"input": input})
    print("Response : ",response.content)
    return jsonify({"bot_reply": response.content})

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=8080, debug=True)