from dotenv import load_dotenv
load_dotenv()

import time
import uuid
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_core.tools import Tool
from agents.tools import tools
from data_ingest.ingest import build_knowledge_base
from agents.escalation import should_escalate, escalation_message
from feedback.feedback_collector import FeedbackCollector

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
            name = "KnowledgeBase",
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

# Initialize feedback collector
feedback_collector = FeedbackCollector()

# Escalation state variables
fallback_count = 0
form_fail_count = 0
repeated_intent_count = 0
last_intent = None
last_response = None

# Session tracking
session_id = str(uuid.uuid4())[:8]

# 5. start a simple interaction
print(f"🤖 HR Bot Session: {session_id}")
print("Type 'exit' to quit, 'stats' to see feedback statistics")

while True:
    user_input = input("You: ")
    if user_input.lower() in ["exit", "quit"]:
        break
    
    if user_input.lower() == "stats":
        stats = feedback_collector.get_feedback_stats()
        print("📊 Feedback Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
        continue

    start_time = time.time()
    
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

    escalation_triggered = False
    if should_escalate(
        confidence=confidence,
        user_input=user_input,
        fallback_count=fallback_count,
        form_fail_count=form_fail_count,
        sentiment=sentiment,
        repeated_intent_count=repeated_intent_count
    ):
        bot_response = escalation_message()
        escalation_triggered = True
        print(f"Bot: {bot_response}")
    else:
        response = agent.invoke({"input": user_input})
        bot_response = response.get('output')
        print(f"Bot: {bot_response}")

    response_time = time.time() - start_time
    
    # Collect feedback
    print("\n📝 How helpful was this response? (1-5, or press Enter to skip)")
    rating_input = input("Rating: ").strip()
    
    if rating_input and rating_input.isdigit():
        rating = int(rating_input)
        if 1 <= rating <= 5:
            feedback_text = input("Additional feedback (optional): ").strip() or None
            
            # Extract tools used from response (simplified)
            tools_used = []
            if "KnowledgeBase" in str(response):
                tools_used.append("KnowledgeBase")
            if "GetLeaveBalance" in str(response):
                tools_used.append("GetLeaveBalance")
            if "CalendarAPI" in str(response):
                tools_used.append("CalendarAPI")
            
            feedback_collector.collect_feedback(
                session_id=session_id,
                user_query=user_input,
                bot_response=bot_response,
                rating=rating,
                feedback_text=feedback_text,
                escalation_triggered=escalation_triggered,
                tools_used=tools_used,
                response_time=response_time
            )
        else:
            print("Invalid rating. Must be 1-5.")
    else:
        print("Feedback skipped.")
    
    print("-" * 50)
    last_response = bot_response
