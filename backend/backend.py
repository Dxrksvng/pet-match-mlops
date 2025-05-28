from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
import os
from openai import OpenAI

load_dotenv()

app = FastAPI()

# Load and split the documents
file_path = "data/all_animal_breeds.csv"
loader = CSVLoader(file_path=file_path)
docs = loader.load_and_split()

# Create an embedding model and index for FAISS
embeddings = OpenAIEmbeddings()
index = faiss.IndexFlatL2(len(OpenAIEmbeddings().embed_query(" ")))
vector_store = FAISS(
    embedding_function=OpenAIEmbeddings(),
    index=index,
    docstore=InMemoryDocstore(),
    index_to_docstore_id={}
)

vector_store.add_documents(documents=docs)
retriever = vector_store.as_retriever()

# Define the LLM and chain for pet recommendations
llm_rec = ChatOpenAI(model="gpt-4o-mini")
system_prompt = (
    """You are an Expert Pet Selection Assistant. You are helping a user find the best pet for their lifestyle.
    You must:
    1. Use only the information from {context}.
    2. Respond in a friendly tone in Thai.
    3. Recommend 3 breeds with reasons.
    4. Apologize if no data is found.
    5. Answer with decorative emoji.
    """
)

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
])

question_answer_chain = create_stuff_documents_chain(llm_rec, prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


class PetRequest(BaseModel):
    preferences: str


class ChatRequest(BaseModel):
    input_text: str
    history: list


# General chat functionality
@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        input_text = request.input_text
        history = request.history

        # Initialize general LLM model for chat
        llm_genral = OpenAI()

        # Generate chat response
        response = llm_genral.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system", 
                    "content": f"You are a helpful assistant for pets recommendation. You must respond in a friendly tone in Thai with decorate emoji and scope based on the chat history {history}."
                },
                {"role": "user", "content": input_text}
            ]
        )

        # Append the new interaction to the history and return the response
        return {"history": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


# Pet recommendation functionality
@app.post("/recommend")
async def get_recommendation(request: PetRequest):
    try:
        # Generate the pet recommendation based on user preferences
        input_text = request.preferences
        answer = rag_chain.invoke({"input": input_text, "context": "all_animal_breeds"})
        return {"recommendation": answer['answer']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=80)
