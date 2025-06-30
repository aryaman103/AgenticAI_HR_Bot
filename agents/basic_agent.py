from dotenv import load_dotenv
load_dotenv()

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import Tool
from agents.tools import tools
from data_ingest.ingest import build_knowledge_base

# 1. initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 2. define memory so the agent remembers the conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 3. Add knowledge base tool (LlamaIndex)
try:
    index = build_knowledge_base()
    def knowledge_base_tool(query: str) -> str:
        retriever = index.as_retriever(similarity_top_k=3)
        results = retriever.retrieve(query)
        if not results:
            return "No relevant information found in the knowledge base."
        return "\n".join([r.get_content() for r in results])
    tools.append(
        Tool(
            name="KnowledgeBase",
            func=knowledge_base_tool,
            description="Semantic search over HR documents."
        )
    )
except Exception as e:
    print("Knowledge base not available:", e)

# 4. initialize the agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
    memory=memory,
    verbose=True,
    handle_parsing_errors=True,
)

# 5. Start a simple interaction
test_input = "I'm going on vacation next month, how do I apply and check how many days I have left?"
response = agent.invoke({"input": test_input})

print(f"Input: {response.get('input')}")
print("Chat History:")
for msg in response.get("chat_history", []):
    print(f"  {msg.type.capitalize()}: {msg.content}")
print(f"Output: {response.get('output')}")
