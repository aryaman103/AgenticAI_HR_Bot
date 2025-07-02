from dotenv import load_dotenv
load_dotenv()

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import Tool
from agents.tools import tools
from data_ingest.ingest import build_knowledge_base
from agents.escalation import should_escalate, escalation_message

# 1. initialize the LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# 2. define memory so the agent remembers the conversation
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# 3. add knowledge base tool (LlamaIndex)
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
            description="Semantic search over HR documents (leave application, leave balance, holidays, etc.)."
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

# Escalation state variables
fallback_count = 0
form_fail_count = 0
repeated_intent_count = 0
last_intent = None
last_response = None

# 5. start a simple interaction
while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break

    # --- STUBS: Replace with real intent/sentiment/confidence logic ---
    confidence = 0.7  # Replace with real intent confidence
    sentiment = "neutral"  # Replace with real sentiment classifier
    intent = "general"  # Replace with real intent detection
    response = None

    # Example fallback detection (stub):
    # If the agent can't answer, increment fallback_count
    # Here, we just reset for demo
    fallback_count = 0

    # Example repeated intent/loop detection (stub):
    if last_intent == intent:
        repeated_intent_count += 1
    else:
        repeated_intent_count = 0
    last_intent = intent

    # Example form fail detection (stub):
    # If user fails to provide required info, increment form_fail_count
    # Here, we just reset for demo
    form_fail_count = 0

    if should_escalate(
        confidence=confidence,
        user_input=user_input,
        fallback_count=fallback_count,
        form_fail_count=form_fail_count,
        sentiment=sentiment,
        repeated_intent_count=repeated_intent_count
    ):
        print(f"Bot: {escalation_message()}")
        continue

    response = agent.invoke({"input": user_input})
    print(f"Bot: {response.get('output')}")
    last_response = response.get('output')
