from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory

def get_buffer_memory():
    """Full chat history memory."""
    return ConversationBufferMemory(memory_key="chat_history", return_messages=True)

def get_summary_memory(llm):
    """Summarizes long conversations (requires an LLM)."""
    return ConversationSummaryMemory(memory_key="summary", llm=llm)

 