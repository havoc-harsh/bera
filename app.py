from flask import Flask, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

# Retrieve needed environment variables
PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# Import your chain/helper code
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from src.prompt import system_prompt

app = Flask(__name__)
CORS(app)

# 1. Load embeddings
embeddings = download_hugging_face_embeddings()

# 2. Create vector store retriever
index_name = "drbera"
docsearch = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# 3. Initialize LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro-001",
    google_api_key=GEMINI_API_KEY,
    temperature=0.4,
    max_tokens=500
)

# 4. Create chain(s)
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("human", "{input}")
    ]
)
question_answer_chain = create_stuff_documents_chain(llm, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)

# Only ONE route for /get
@app.route("/get", methods=["POST"])
def chat():
    # Read form data (since React sends formData with 'msg')
    msg = request.form.get("msg")
    print("Received message:", msg)

    # Run it through your RAG chain
    response = rag_chain.invoke({"input": msg})
    answer = response["answer"]
    print("Response:", answer)

    # Return just the string answer
    return str(answer)

# Optional home route (not mandatory)
@app.route("/")
def home():
    return "Server is running."

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True) 
