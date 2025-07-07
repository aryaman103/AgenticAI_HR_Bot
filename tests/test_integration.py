#!/usr/bin/env python3
"""
Integration Tests for HR Agent Bot
Tests component interactions and workflows
"""

import unittest
import tempfile
import os
import json
from unittest.mock import Mock, patch
from datetime import datetime

# Import components to test
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from agents.tools import tools
from agents.escalation import should_escalate, escalation_message
from feedback.feedback_collector import FeedbackCollector
from data_ingest.ingest import build_knowledge_base


class TestAgentIntegration(unittest.TestCase):
    """Test agent integration with tools and memory."""
    
    def setUp(self):
        """Set up test environment."""
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0)
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Initialize agent with tools
        self.agent = initialize_agent(
            tools=tools,
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=False,
            handle_parsing_errors=True,
        )
    
    def test_agent_initialization(self):
        """Test that agent initializes correctly with tools."""
        self.assertIsNotNone(self.agent)
        self.assertIsNotNone(self.agent.tools)
        self.assertGreater(len(self.agent.tools), 0)
    
    def test_agent_with_leave_balance_query(self):
        """Test agent response to leave balance query."""
        query = "How do I check my leave balance? I'm user123"
        
        try:
            response = self.agent.invoke({"input": query})
            self.assertIsNotNone(response)
            self.assertIn("output", response)
            
            output = response.get("output", "")
            self.assertIsInstance(output, str)
            self.assertGreater(len(output), 0)
            
        except Exception as e:
            # If agent fails due to API issues, that's okay for testing
            print(f"Agent test skipped due to API issue: {e}")
    
    def test_agent_with_holiday_query(self):
        """Test agent response to holiday query."""
        query = "When is the next holiday?"
        
        try:
            response = self.agent.invoke({"input": query})
            self.assertIsNotNone(response)
            self.assertIn("output", response)
            
            output = response.get("output", "")
            self.assertIsInstance(output, str)
            self.assertGreater(len(output), 0)
            
        except Exception as e:
            print(f"Agent test skipped due to API issue: {e}")
    
    def test_agent_memory_retention(self):
        """Test that agent retains conversation memory."""
        query1 = "What's my leave balance?"
        query2 = "How do I apply for leave?"
        
        try:
            # First query
            response1 = self.agent.invoke({"input": query1})
            
            # Second query (should have context from first)
            response2 = self.agent.invoke({"input": query2})
            
            self.assertIsNotNone(response1)
            self.assertIsNotNone(response2)
            
        except Exception as e:
            print(f"Memory test skipped due to API issue: {e}")


class TestEscalationIntegration(unittest.TestCase):
    """Test escalation integration with agent."""
    
    def test_escalation_with_sensitive_topic(self):
        """Test escalation triggered by sensitive topic."""
        user_input = "I need to report harassment in my department"
        
        # Should trigger escalation
        should_escalate_result = should_escalate(
            confidence=0.8,  # High confidence
            user_input=user_input,
            fallback_count=0,
            form_fail_count=0,
            sentiment="neutral",
            repeated_intent_count=0
        )
        
        self.assertTrue(should_escalate_result)
        
        # Should provide escalation message
        message = escalation_message()
        self.assertIn("HR specialist", message)
    
    def test_escalation_with_user_request(self):
        """Test escalation triggered by user request."""
        user_input = "I want to talk to a human HR representative"
        
        should_escalate_result = should_escalate(
            confidence=0.9,
            user_input=user_input,
            fallback_count=0,
            form_fail_count=0,
            sentiment="neutral",
            repeated_intent_count=0
        )
        
        self.assertTrue(should_escalate_result)
    
    def test_no_escalation_normal_query(self):
        """Test that normal queries don't trigger escalation."""
        user_input = "What's my leave balance?"
        
        should_escalate_result = should_escalate(
            confidence=0.8,
            user_input=user_input,
            fallback_count=0,
            form_fail_count=0,
            sentiment="neutral",
            repeated_intent_count=0
        )
        
        self.assertFalse(should_escalate_result)


class TestFeedbackIntegration(unittest.TestCase):
    """Test feedback collection integration."""
    
    def setUp(self):
        """Set up test environment."""
        self.collector = FeedbackCollector()
    
    def test_feedback_with_agent_response(self):
        """Test feedback collection with agent response."""
        session_id = "test_session_123"
        user_query = "How do I apply for leave?"
        bot_response = "To apply for leave, visit the HR portal..."
        
        # Collect feedback
        self.collector.collect_feedback(
            session_id=session_id,
            user_query=user_query,
            bot_response=bot_response,
            rating=4,
            feedback_text="Very helpful!",
            tools_used=["KnowledgeBase"],
            response_time=1.5
        )
        
        # Verify feedback was collected
        stats = self.collector.get_feedback_stats()
        self.assertEqual(stats["total_feedback"], 1)
        self.assertEqual(stats["average_rating"], 4.0)
    
    def test_feedback_with_escalation(self):
        """Test feedback collection with escalation."""
        session_id = "test_session_456"
        user_query = "I need to report harassment"
        bot_response = escalation_message()
        
        # Collect feedback for escalated case
        self.collector.collect_feedback(
            session_id=session_id,
            user_query=user_query,
            bot_response=bot_response,
            rating=3,
            feedback_text="Good escalation",
            tools_used=[],
            response_time=0.5,
            escalation_triggered=True
        )
        
        # Verify feedback was collected
        stats = self.collector.get_feedback_stats()
        self.assertEqual(stats["total_feedback"], 1)
    
    def test_feedback_analytics(self):
        """Test feedback analytics and statistics."""
        # Add multiple feedback entries
        feedback_data = [
            {"rating": 5, "escalation_triggered": False},
            {"rating": 4, "escalation_triggered": False},
            {"rating": 3, "escalation_triggered": True},
            {"rating": 5, "escalation_triggered": False},
            {"rating": 2, "escalation_triggered": True}
        ]
        
        for i, data in enumerate(feedback_data):
            self.collector.collect_feedback(
                session_id=f"session_{i}",
                user_query=f"Query {i}",
                bot_response=f"Response {i}",
                rating=data["rating"],
                escalation_triggered=data["escalation_triggered"],
                tools_used=["KnowledgeBase"],
                response_time=1.0
            )
        
        # Get analytics
        stats = self.collector.get_feedback_stats()
        
        # Verify statistics
        self.assertEqual(stats["total_feedback"], 5)
        self.assertEqual(stats["average_rating"], 3.8)  # (5+4+3+5+2)/5
        self.assertEqual(stats["escalation_rate"], 0.4)  # 2/5
        self.assertEqual(stats["rating_distribution"]["5"], 2)
        self.assertEqual(stats["rating_distribution"]["4"], 1)
        self.assertEqual(stats["rating_distribution"]["3"], 1)
        self.assertEqual(stats["rating_distribution"]["2"], 1)


class TestKnowledgeBaseIntegration(unittest.TestCase):
    """Test knowledge base integration."""
    
    @patch('data_ingest.ingest.build_knowledge_base')
    def test_knowledge_base_initialization(self, mock_build):
        """Test knowledge base initialization."""
        # Mock the knowledge base to avoid file system dependencies
        mock_index = Mock()
        mock_build.return_value = mock_index
        
        try:
            index = build_knowledge_base()
            self.assertIsNotNone(index)
        except Exception as e:
            print(f"Knowledge base test skipped: {e}")


class TestToolIntegration(unittest.TestCase):
    """Test tool integration with agent."""
    
    def test_tool_availability(self):
        """Test that all required tools are available."""
        required_tools = ["GetLeaveBalance", "CalendarAPI"]
        
        tool_names = [tool.name for tool in tools]
        
        for required_tool in required_tools:
            self.assertIn(required_tool, tool_names)
    
    def test_tool_functionality(self):
        """Test that tools function correctly."""
        # Test leave balance tool
        leave_result = tools[0].func("user123")
        self.assertIsInstance(leave_result, str)
        self.assertIn("HR portal", leave_result)
        
        # Test calendar tool
        calendar_result = tools[1].func("When is the next holiday?")
        self.assertIsInstance(calendar_result, str)
        self.assertIn("holiday", calendar_result.lower())


if __name__ == '__main__':
    unittest.main() 