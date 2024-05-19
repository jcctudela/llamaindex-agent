from llama_index.core.tools import FunctionTool
from llama_index.agent.openai import OpenAIAgent
from llama_index.llms.openai import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage

from flask import Flask, request

# Define a function to multiply two integers
def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result"""
    return a * b

# Define a function to add two integers
def add(a: int, b: int) -> int:
    """Add two integers and return the result"""
    return a + b

# Define a function to handle questions using a RAG model
def rag(prompt: str):
    """Answer questions about text messages API usage using RAG model"""
    chat_engine = index.as_chat_engine(
        # llm=OpenAI(model="gpt-3.5-turbo-0613"),
        llm=OpenAI(model="gpt-4o"),
        system_prompt=(
            "You are a chatbot, you only can answer questions related to the documents you have read."
        ),
    )
    response = chat_engine.chat(prompt)

    return response.response

# Initialize the RAG model and index
def rag_init():
    global index
    try:
        # Load the storage context from defaults
        storage_context = StorageContext.from_defaults(
            persist_dir="./storage/context"
        )
        # Load the index from storage
        index = load_index_from_storage(storage_context)

        index_loaded = True
    except:
        index_loaded = False

    if not index_loaded:
        print("Index not found, creating a new one...")
        # Load data from the input directory
        data = SimpleDirectoryReader(input_dir="./input_files/").load_data()

        # Build the index from documents
        index = VectorStoreIndex.from_documents(data)

        # Persist the index to the storage context
        index.storage_context.persist(persist_dir="./storage/context")

# Asynchronous function to handle agent interactions
def agent(prompt: str):
    multiply_tool = FunctionTool.from_defaults(fn=multiply)
    add_tool = FunctionTool.from_defaults(fn=add)
    rag_tool = FunctionTool.from_defaults(fn=rag)

    # llm = OpenAI(model="gpt-3.5-turbo-0613")
    # llm = OpenAI(model="gpt-4-turbo")
    llm = OpenAI(model="gpt-4o")
    # Initialize the OpenAI agent with tools and model
    agent = OpenAIAgent.from_tools(
        [multiply_tool, add_tool, rag_tool],
        llm=llm,
        verbose=True,
        system_prompt="You are a chatbot, you only can answer questions related to tools you have. "
                      "If any question outside those tools, you must say "
                      "'I only can answer questions about the messaging API usage'"
    )

    # Get response from the agent
    response = agent.chat(prompt)

    return response.response

# Initialize the Flask application
app = Flask(__name__)

@app.route('/', methods=['POST'])
def home():
    # Accessing the data sent with the POST request
    if request.is_json:
        data = request.get_json()
        text = data.get("prompt", "")
        # Get result from the agent
        result = agent(text)
        return result
    else:
        return "Please send JSON data.", 400

def main():
    # Initialize RAG model and index
    rag_init()
    # Run the Flask app
    app.run(host='0.0.0.0', port=8000)

# Entry point of the script
if __name__ == '__main__':
    main()


# curl -X POST http://localhost:8000/ -H "Content-Type: application/json" -d '{"prompt": "cuanto es 5 por 8 mas 23 y despues me dices si existe un endpoint de añadir un grupo en la api de mensajeria"}'