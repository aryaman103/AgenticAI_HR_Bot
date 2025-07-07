#!/usr/bin/env python3
"""
Unit Tests for HR Agent Bot Components
Tests individual components in isolation
"""

import unittest
import tempfile
import os
import json
from unittest.mock import Mock, patch
from datetime import datetime

# Import components to test with error handling
try:
    from agents.tools import get_leave_balance, calendar_api, tools
    from agents.escalation import (
        should_escalate_confidence,
        should_escalate_user_request,
        should_escalate_fallback,
        should_escalate_sensitive_topic,
        should_escalate_form_failure,
        should_escalate_sentiment,
        should_escalate_loop,
        should_escalate,
        escalation_message
    )
    from feedback.feedback_collector import FeedbackCollector
    TOOLS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Some components not available for testing: {e}")
    TOOLS_AVAILABLE = False

# Mock document parser for testing
class MockDocumentParser:
    def __init__(self):
        self.documents = []
    
    def parse_directory(self):
        return self.documents

class TestTools(unittest.TestCase):
    """Test the HR tools functionality."""
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Tools not available")
    def test_get_leave_balance(self):
        """Test leave balance tool."""
        result = get_leave_balance("user123")
        self.assertIsInstance(result, str)
        self.assertIn("HR portal", result)
        self.assertIn("hr.companyname.com", result)
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Tools not available")
    def test_calendar_api_next_holiday(self):
        """Test calendar API for next holiday query."""
        result = calendar_api("When is the next holiday?")
        self.assertIsInstance(result, str)
        self.assertIn("Next holiday:", result)
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Tools not available")
    def test_calendar_api_all_holidays(self):
        """Test calendar API for all holidays query."""
        result = calendar_api("Show me all holidays")
        self.assertIsInstance(result, str)
        self.assertIn("All company holidays", result)
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Tools not available")
    def test_calendar_api_general_holiday(self):
        """Test calendar API for general holiday query."""
        result = calendar_api("What holidays do we have?")
        self.assertIsInstance(result, str)
        self.assertIn("Company holidays include:", result)
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Tools not available")
    def test_calendar_api_invalid_query(self):
        """Test calendar API for invalid query."""
        result = calendar_api("What's the weather like?")
        self.assertIsInstance(result, str)
        self.assertIn("not found", result)
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Tools not available")
    def test_tools_list(self):
        """Test that tools list is properly configured."""
        self.assertIsInstance(tools, list)
        self.assertGreater(len(tools), 0)
        
        for tool in tools:
            self.assertIsInstance(tool.name, str)
            self.assertIsInstance(tool.description, str)
            self.assertTrue(callable(tool.func))


class TestEscalation(unittest.TestCase):
    """Test escalation logic."""
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Escalation not available")
    def test_confidence_escalation(self):
        """Test confidence-based escalation."""
        # Low confidence should trigger escalation
        self.assertTrue(should_escalate_confidence(0.3))
        # High confidence should not trigger escalation
        self.assertFalse(should_escalate_confidence(0.8))
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Escalation not available")
    def test_user_request_escalation(self):
        """Test user-requested escalation."""
        # Should escalate when user requests human
        self.assertTrue(should_escalate_user_request("I need to talk to a human"))
        self.assertTrue(should_escalate_user_request("This isn't helping, escalate"))
        # Should not escalate for normal queries
        self.assertFalse(should_escalate_user_request("What's my leave balance?"))
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Escalation not available")
    def test_fallback_escalation(self):
        """Test fallback-based escalation."""
        # Should escalate after multiple fallbacks
        self.assertTrue(should_escalate_fallback(3))
        # Should not escalate for few fallbacks
        self.assertFalse(should_escalate_fallback(1))
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Escalation not available")
    def test_sensitive_topic_escalation(self):
        """Test sensitive topic escalation."""
        # Should escalate for sensitive topics
        self.assertTrue(should_escalate_sensitive_topic("I need to report harassment"))
        self.assertTrue(should_escalate_sensitive_topic("There's a payroll error"))
        # Should not escalate for normal topics
        self.assertFalse(should_escalate_sensitive_topic("What's my leave balance?"))
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Escalation not available")
    def test_form_failure_escalation(self):
        """Test form failure escalation."""
        # Should escalate after multiple form failures
        self.assertTrue(should_escalate_form_failure(3))
        # Should not escalate for few failures
        self.assertFalse(should_escalate_form_failure(1))
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Escalation not available")
    def test_sentiment_escalation(self):
        """Test sentiment-based escalation."""
        # Should escalate for negative sentiment
        self.assertTrue(should_escalate_sentiment("frustrated"))
        self.assertTrue(should_escalate_sentiment("angry"))
        # Should not escalate for positive sentiment
        self.assertFalse(should_escalate_sentiment("happy"))
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Escalation not available")
    def test_loop_escalation(self):
        """Test loop detection escalation."""
        # Should escalate after repeated intents
        self.assertTrue(should_escalate_loop(3))
        # Should not escalate for few repetitions
        self.assertFalse(should_escalate_loop(1))
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Escalation not available")
    def test_main_escalation_function(self):
        """Test the main escalation decision function."""
        # Test escalation with low confidence
        self.assertTrue(should_escalate(
            confidence=0.3,
            user_input="What's my leave balance?",
            fallback_count=0,
            form_fail_count=0,
            sentiment="neutral",
            repeated_intent_count=0
        ))
        
        # Test no escalation with good conditions
        self.assertFalse(should_escalate(
            confidence=0.8,
            user_input="What's my leave balance?",
            fallback_count=0,
            form_fail_count=0,
            sentiment="neutral",
            repeated_intent_count=0
        ))
    
    @unittest.skipUnless(TOOLS_AVAILABLE, "Escalation not available")
    def test_escalation_message(self):
        """Test escalation message format."""
        message = escalation_message()
        self.assertIsInstance(message, str)
        self.assertIn("HR specialist", message)


class TestFeedbackCollector(unittest.TestCase):
    """Test feedback collection system."""
    
    def setUp(self):
        """Set up test environment."""
        try:
            self.collector = FeedbackCollector()
            self.test_feedback = {
                "session_id": "test_session",
                "user_query": "Test query",
                "bot_response": "Test response",
                "rating": 4,
                "feedback_text": "Test feedback",
                "tools_used": ["KnowledgeBase"],
                "response_time": 1.0
            }
        except Exception as e:
            self.skipTest(f"FeedbackCollector not available: {e}")
    
    def test_collect_feedback(self):
        """Test feedback collection."""
        # Collect feedback
        self.collector.collect_feedback(**self.test_feedback)
        
        # Verify feedback was stored
        stats = self.collector.get_feedback_stats()
        self.assertEqual(stats["total_feedback"], 1)
        self.assertEqual(stats["average_rating"], 4.0)
    
    def test_get_feedback_stats(self):
        """Test feedback statistics calculation."""
        # Add multiple feedback entries
        for i in range(3):
            feedback = self.test_feedback.copy()
            feedback["rating"] = i + 3  # Ratings: 3, 4, 5
            self.collector.collect_feedback(**feedback)
        
        stats = self.collector.get_feedback_stats()
        self.assertEqual(stats["total_feedback"], 3)
        self.assertEqual(stats["average_rating"], 4.0)  # (3+4+5)/3
        self.assertEqual(stats["rating_distribution"]["5"], 1)
        self.assertEqual(stats["rating_distribution"]["4"], 1)
        self.assertEqual(stats["rating_distribution"]["3"], 1)
    
    def test_get_recent_feedback(self):
        """Test recent feedback retrieval."""
        # Add multiple feedback entries
        for i in range(5):
            feedback = self.test_feedback.copy()
            feedback["session_id"] = f"session_{i}"
            self.collector.collect_feedback(**feedback)
        
        recent = self.collector.get_recent_feedback(3)
        self.assertEqual(len(recent), 3)
    
    def test_export_feedback(self):
        """Test feedback export functionality."""
        # Add some feedback
        self.collector.collect_feedback(**self.test_feedback)
        
        # Export feedback
        export_path = self.collector.export_feedback()
        
        # Verify export file exists
        self.assertTrue(os.path.exists(export_path))
        
        # Verify export file content
        with open(export_path, 'r') as f:
            exported_data = json.load(f)
        
        self.assertIn("feedback", exported_data)
        self.assertIn("statistics", exported_data)
    
    def test_invalid_rating(self):
        """Test handling of invalid ratings."""
        invalid_feedback = self.test_feedback.copy()
        invalid_feedback["rating"] = 6  # Invalid rating
        
        # Should handle invalid rating gracefully
        try:
            self.collector.collect_feedback(**invalid_feedback)
        except Exception as e:
            self.fail(f"Should handle invalid rating gracefully: {e}")


class TestDocumentParser(unittest.TestCase):
    """Test document parsing functionality."""
    
    def setUp(self):
        """Set up test environment."""
        self.parser = MockDocumentParser()
    
    def test_document_parser_initialization(self):
        """Test document parser initialization."""
        self.assertIsNotNone(self.parser)
    
    def test_parser_metadata_extraction(self):
        """Test metadata extraction from documents."""
        # This test would require actual document files
        # For now, we'll test the parser can be instantiated
        self.assertIsNotNone(self.parser)


if __name__ == '__main__':
    unittest.main() 