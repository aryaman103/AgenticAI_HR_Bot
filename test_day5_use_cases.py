#!/usr/bin/env python3
"""
Day 5: Prototype HR Use Cases Test Script
Tests the three main HR use cases:
1. Leave balance inquiry
2. Holiday calendar lookup  
3. Leave application guidance
"""

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from agents.tools import tools

def test_hr_use_cases():
    """Test the three main HR use cases."""
    
    # Initialize the agent
    llm = ChatOpenAI(model="gpt-4o", temperature=0)
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
    )
    
    print("🤖 HR Bot - Day 5 Use Cases Test")
    print("=" * 50)
    
    # Test Case 1: Leave Balance Inquiry
    print("\n📊 TEST CASE 1: Leave Balance Inquiry")
    print("-" * 30)
    test_input_1 = "What's my current leave balance? I'm user123"
    print(f"User: {test_input_1}")
    
    response_1 = agent.invoke({"input": test_input_1})
    print(f"Bot: {response_1.get('output')}")
    
    # Test Case 2: Holiday Calendar Lookup
    print("\n📅 TEST CASE 2: Holiday Calendar Lookup")
    print("-" * 30)
    test_input_2 = "When is the next company holiday?"
    print(f"User: {test_input_2}")
    
    response_2 = agent.invoke({"input": test_input_2})
    print(f"Bot: {response_2.get('output')}")
    
    # Test Case 3: Leave Application Guidance
    print("\n📝 TEST CASE 3: Leave Application Guidance")
    print("-" * 30)
    test_input_3 = "I want to apply for vacation next month. How do I do it?"
    print(f"User: {test_input_3}")
    
    response_3 = agent.invoke({"input": test_input_3})
    print(f"Bot: {response_3.get('output')}")
    
    # Test Case 4: Complex Multi-step Query (Bonus)
    print("\n🔄 TEST CASE 4: Complex Multi-step Query")
    print("-" * 30)
    test_input_4 = "I'm going on vacation next month, how do I apply and check how many days I have left?"
    print(f"User: {test_input_4}")
    
    response_4 = agent.invoke({"input": test_input_4})
    print(f"Bot: {response_4.get('output')}")
    
    print("\n" + "=" * 50)
    print("✅ Day 5 Use Cases Test Complete!")
    print("\nSummary of capabilities demonstrated:")
    print("✓ Leave balance inquiry with employee lookup")
    print("✓ Holiday calendar lookup with date calculations")
    print("✓ Leave application guidance with step-by-step process")
    print("✓ Complex multi-step queries using multiple tools")
    print("✓ Memory retention across conversation")

if __name__ == "__main__":
    test_hr_use_cases() 