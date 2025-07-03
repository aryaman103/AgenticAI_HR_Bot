"""
Feedback Collection System for HR Bot
Collects user feedback for continuous improvement
"""

import json
import datetime
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict

@dataclass
class FeedbackEntry:
    """Structure for feedback data."""
    timestamp: str
    session_id: str
    user_query: str
    bot_response: str
    rating: int  # 1-5 scale
    feedback_text: Optional[str] = None
    escalation_triggered: bool = False
    tools_used: List[str] = None
    response_time: float = 0.0

class FeedbackCollector:
    """Collects and stores user feedback."""
    
    def __init__(self, feedback_dir: str = "./feedback"):
        self.feedback_dir = Path(feedback_dir)
        self.feedback_dir.mkdir(exist_ok=True)
        self.feedback_file = self.feedback_dir / "feedback_data.json"
        self.session_file = self.feedback_dir / "session_data.json"
        
        # Initialize files if they don't exist
        if not self.feedback_file.exists():
            self._save_feedback([])
        if not self.session_file.exists():
            self._save_sessions({})
    
    def collect_feedback(
        self,
        session_id: str,
        user_query: str,
        bot_response: str,
        rating: int,
        feedback_text: Optional[str] = None,
        escalation_triggered: bool = False,
        tools_used: List[str] = None,
        response_time: float = 0.0
    ) -> bool:
        """Collect feedback for a bot interaction."""
        
        if not 1 <= rating <= 5:
            print("Rating must be between 1 and 5")
            return False
        
        feedback_entry = FeedbackEntry(
            timestamp=datetime.datetime.now().isoformat(),
            session_id=session_id,
            user_query=user_query,
            bot_response=bot_response,
            rating=rating,
            feedback_text=feedback_text,
            escalation_triggered=escalation_triggered,
            tools_used=tools_used or [],
            response_time=response_time
        )
        
        # Load existing feedback
        feedback_data = self._load_feedback()
        feedback_data.append(asdict(feedback_entry))
        
        # Save updated feedback
        self._save_feedback(feedback_data)
        
        print(f"✓ Feedback collected: Rating {rating}/5")
        return True
    
    def get_feedback_stats(self) -> Dict:
        """Get statistics about collected feedback."""
        feedback_data = self._load_feedback()
        
        if not feedback_data:
            return {"total_feedback": 0}
        
        total = len(feedback_data)
        ratings = [entry["rating"] for entry in feedback_data]
        avg_rating = sum(ratings) / len(ratings)
        
        escalation_count = sum(1 for entry in feedback_data if entry["escalation_triggered"])
        
        # Most common tools used
        all_tools = []
        for entry in feedback_data:
            all_tools.extend(entry.get("tools_used", []))
        
        tool_counts = {}
        for tool in all_tools:
            tool_counts[tool] = tool_counts.get(tool, 0) + 1
        
        return {
            "total_feedback": total,
            "average_rating": round(avg_rating, 2),
            "escalation_rate": round(escalation_count / total * 100, 2),
            "tool_usage": tool_counts,
            "rating_distribution": {
                "1": ratings.count(1),
                "2": ratings.count(2),
                "3": ratings.count(3),
                "4": ratings.count(4),
                "5": ratings.count(5)
            }
        }
    
    def get_recent_feedback(self, limit: int = 10) -> List[Dict]:
        """Get recent feedback entries."""
        feedback_data = self._load_feedback()
        return feedback_data[-limit:] if feedback_data else []
    
    def export_feedback(self, filename: str = None) -> str:
        """Export feedback data to a file."""
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"feedback_export_{timestamp}.json"
        
        export_path = self.feedback_dir / filename
        feedback_data = self._load_feedback()
        
        with open(export_path, 'w') as f:
            json.dump(feedback_data, f, indent=2)
        
        return str(export_path)
    
    def _load_feedback(self) -> List[Dict]:
        """Load feedback data from file."""
        try:
            with open(self.feedback_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def _save_feedback(self, feedback_data: List[Dict]):
        """Save feedback data to file."""
        with open(self.feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=2)
    
    def _save_sessions(self, session_data: Dict):
        """Save session data to file."""
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=2)

# Example usage
if __name__ == "__main__":
    collector = FeedbackCollector()
    
    # Example feedback collection
    collector.collect_feedback(
        session_id="session_123",
        user_query="How do I apply for leave?",
        bot_response="To apply for leave, visit the HR portal...",
        rating=4,
        feedback_text="Very helpful response!",
        tools_used=["KnowledgeBase"],
        response_time=1.2
    )
    
    # Get stats
    stats = collector.get_feedback_stats()
    print("Feedback Statistics:")
    print(json.dumps(stats, indent=2)) 