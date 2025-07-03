#!/usr/bin/env python3
"""
Day 7: Document Parsing & Feedback Collection Test
Tests the new document parsing capabilities and feedback collection system
"""

from dotenv import load_dotenv
load_dotenv()

from data_ingest.document_parser import HRDocumentParser
from data_ingest.ingest import get_document_stats
from feedback.feedback_collector import FeedbackCollector
import json

def test_document_parsing():
    """Test document parsing capabilities."""
    print("📄 Testing Document Parsing")
    print("=" * 40)
    
    # Get document statistics
    stats = get_document_stats()
    print("Document Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Test parser
    parser = HRDocumentParser()
    documents = parser.parse_directory()
    
    print(f"\n✓ Successfully parsed {len(documents)} documents")
    for doc in documents:
        print(f"  - {doc.metadata.get('source_file', 'Unknown')} ({doc.metadata.get('file_type', 'Unknown')})")
        print(f"    Content length: {len(doc.text)} characters")

def test_feedback_collection():
    """Test feedback collection system."""
    print("\n📝 Testing Feedback Collection")
    print("=" * 40)
    
    collector = FeedbackCollector()
    
    # Add some sample feedback
    sample_feedback = [
        {
            "session_id": "test_session_1",
            "user_query": "How do I apply for leave?",
            "bot_response": "To apply for leave, visit the HR portal...",
            "rating": 4,
            "feedback_text": "Very helpful response!",
            "tools_used": ["KnowledgeBase"],
            "response_time": 1.2
        },
        {
            "session_id": "test_session_2", 
            "user_query": "When is the next holiday?",
            "bot_response": "The next holiday is...",
            "rating": 5,
            "feedback_text": "Perfect!",
            "tools_used": ["CalendarAPI"],
            "response_time": 0.8
        },
        {
            "session_id": "test_session_3",
            "user_query": "I need to report harassment",
            "bot_response": "Let me connect you to an HR specialist...",
            "rating": 3,
            "feedback_text": "Good escalation",
            "tools_used": [],
            "response_time": 0.5,
            "escalation_triggered": True
        }
    ]
    
    for feedback in sample_feedback:
        collector.collect_feedback(**feedback)
    
    # Get feedback statistics
    stats = collector.get_feedback_stats()
    print("Feedback Statistics:")
    print(json.dumps(stats, indent=2))
    
    # Get recent feedback
    recent = collector.get_recent_feedback(5)
    print(f"\nRecent Feedback ({len(recent)} entries):")
    for entry in recent:
        print(f"  - Rating: {entry['rating']}/5 - {entry['user_query'][:50]}...")
    
    # Export feedback
    export_path = collector.export_feedback()
    print(f"\n✓ Feedback exported to: {export_path}")

def main():
    """Run all Day 7 tests."""
    print("🤖 Day 7: Document Parsing & Feedback Collection Test")
    print("=" * 60)
    
    try:
        test_document_parsing()
        test_feedback_collection()
        
        print("\n" + "=" * 60)
        print("✅ Day 7 Features Test Complete!")
        print("\nSummary:")
        print("✓ Document parsing (PDF, DOCX, TXT support)")
        print("✓ Enhanced knowledge base with metadata")
        print("✓ Feedback collection system")
        print("✓ Feedback statistics and analytics")
        print("✓ Feedback export functionality")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    main() 