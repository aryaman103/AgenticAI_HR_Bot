from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
# Uncomment the following lines if you want to use vector memory in the future
# from langchain.memory.vectorstore import VectorStoreRetrieverMemory
# from langchain.vectorstores import FAISS
# from langchain_openai import OpenAIEmbeddings

def get_buffer_memory():
    """Full chat history memory."""
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def get_summary_memory(llm):
    """Summarizes long conversations (requires an LLM)."""
    return ConversationSummaryMemory(memory_key="summary", llm=llm)

# Example for vector memory (advanced, optional)
# def get_vector_memory():
#     embeddings = OpenAIEmbeddings()
#     vectorstore = FAISS(embedding_function=embeddings)
#     return VectorStoreRetrieverMemory(retriever=vectorstore.as_retriever()) 