from src.helper import load_pdfs, download_embedding, filter_to_minimal_docs, text_split
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore
from pinecone import ServerlessSpec
from pinecone import Pinecone
import os

load_dotenv()
PINECONE_API_KEY=os.getenv("PINECONE_API_KEY")
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")

os.environ["PINECONE_API_KEY"]=PINECONE_API_KEY
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY

extracted_data=load_pdfs("data/")
filter_data=filter_to_minimal_docs(extracted_data)
text_chunks=text_split(filter_data)

embeddings=download_embedding()


pinecone_api_key=PINECONE_API_KEY
pc=Pinecone(api_key=pinecone_api_key)


index_name="medical-chatbot"

if not pc.has_index(index_name):
    pc.create_index(
        name=index_name,
        dimension=384,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region ="us-east-1")
    
    )
index=pc.Index(index_name)


doc_search=PineconeVectorStore.from_documents(
    documents=text_chunks,
    embedding=embeddings,
    index_name=index_name
)