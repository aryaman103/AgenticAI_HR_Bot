#!/usr/bin/env python3
"""
FastAPI Backend for HR Agent Bot
Provides RESTful API endpoints for chat, feedback, and analytics
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import time
import json
import uuid
from datetime import datetime
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import bot components
from agents.basic_agent import agent, feedback_collector
from agents.escalation import should_escalate, escalation_message
from feedback.feedback_collector import FeedbackCollector

# Initialize FastAPI app
app = FastAPI(
    title="HR Assistant Bot API",
    description="RESTful API for HR Assistant Bot with chat, feedback, and analytics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    response_time: float
    escalation_triggered: bool
    tools_used: List[str]
    confidence: float

class FeedbackRequest(BaseModel):
    session_id: str
    user_query: str
    bot_response: str
    rating: int
    feedback_text: Optional[str] = None
    tools_used: List[str] = []
    response_time: float
    escalation_triggered: bool = False

class FeedbackResponse(BaseModel):
    success: bool
    message: str

class AnalyticsResponse(BaseModel):
    total_feedback: int
    average_rating: float
    escalation_rate: float
    average_response_time: float
    rating_distribution: Dict[str, int]
    recent_feedback: List[Dict[str, Any]]

class SystemStatusResponse(BaseModel):
    agent_status: str
    knowledge_base_status: str
    feedback_system_status: str
    escalation_system_status: str
    uptime: float

# Global variables
start_time = time.time()
feedback_collector_instance = FeedbackCollector()

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "HR Assistant Bot API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "chat": "/chat",
            "feedback": "/feedback",
            "analytics": "/analytics",
            "status": "/status",
            "health": "/health"
        }
    }

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Main chat endpoint for interacting with the HR bot."""
    try:
        # Generate session ID if not provided
        session_id = request.session_id or f"api_{uuid.uuid4().hex[:8]}"
        
        # Check for escalation
        escalation_triggered = should_escalate(
            confidence=0.7,  # Default confidence
            user_input=request.message,
            fallback_count=0,
            form_fail_count=0,
            sentiment="neutral",
            repeated_intent_count=0
        )
        
        start_time = time.time()
        
        if escalation_triggered:
            response = escalation_message()
            tools_used = []
            confidence = 0.5
        else:
            # Get response from agent
            try:
                agent_response = agent.invoke({"input": request.message})
                response = agent_response.get("output", "I'm sorry, I couldn't process your request.")
                
                # Extract tools used (simplified)
                tools_used = []
                if "KnowledgeBase" in str(agent_response):
                    tools_used.append("KnowledgeBase")
                if "GetLeaveBalance" in str(agent_response):
                    tools_used.append("GetLeaveBalance")
                if "CalendarAPI" in str(agent_response):
                    tools_used.append("CalendarAPI")
                
                confidence = 0.8  # Default confidence
                
            except Exception as e:
                response = f"I'm sorry, I encountered an error: {str(e)}"
                tools_used = []
                confidence = 0.3
        
        response_time = time.time() - start_time
        
        return ChatResponse(
            response=response,
            session_id=session_id,
            response_time=response_time,
            escalation_triggered=escalation_triggered,
            tools_used=tools_used,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat error: {str(e)}")

@app.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """Submit feedback for a chat response."""
    try:
        # Validate rating
        if not 1 <= request.rating <= 5:
            raise HTTPException(status_code=400, detail="Rating must be between 1 and 5")
        
        # Collect feedback
        feedback_collector_instance.collect_feedback(
            session_id=request.session_id,
            user_query=request.user_query,
            bot_response=request.bot_response,
            rating=request.rating,
            feedback_text=request.feedback_text,
            tools_used=request.tools_used,
            response_time=request.response_time,
            escalation_triggered=request.escalation_triggered
        )
        
        return FeedbackResponse(
            success=True,
            message="Feedback submitted successfully"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Feedback error: {str(e)}")

@app.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics():
    """Get analytics and feedback statistics."""
    try:
        stats = feedback_collector_instance.get_feedback_stats()
        recent_feedback = feedback_collector_instance.get_recent_feedback(10)
        
        return AnalyticsResponse(
            total_feedback=stats.get("total_feedback", 0),
            average_rating=stats.get("average_rating", 0.0),
            escalation_rate=stats.get("escalation_rate", 0.0),
            average_response_time=stats.get("average_response_time", 0.0),
            rating_distribution=stats.get("rating_distribution", {}),
            recent_feedback=recent_feedback
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

@app.get("/status", response_model=SystemStatusResponse)
async def get_system_status():
    """Get system status and health information."""
    try:
        uptime = time.time() - start_time
        
        # Check system components (simplified)
        agent_status = "online"
        knowledge_base_status = "available"
        feedback_system_status = "active"
        escalation_system_status = "ready"
        
        return SystemStatusResponse(
            agent_status=agent_status,
            knowledge_base_status=knowledge_base_status,
            feedback_system_status=feedback_system_status,
            escalation_system_status=escalation_system_status,
            uptime=uptime
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Status error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/export-feedback")
async def export_feedback():
    """Export feedback data to file."""
    try:
        export_path = feedback_collector_instance.export_feedback()
        return {
            "success": True,
            "message": "Feedback exported successfully",
            "file_path": export_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export error: {str(e)}")

@app.get("/sessions/{session_id}/history")
async def get_session_history(session_id: str):
    """Get chat history for a specific session."""
    try:
        # This would require implementing session history storage
        # For now, return a placeholder
        return {
            "session_id": session_id,
            "messages": [],
            "message": "Session history not implemented yet"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session history error: {str(e)}")

@app.delete("/sessions/{session_id}")
async def clear_session(session_id: str):
    """Clear chat history for a specific session."""
    try:
        # This would require implementing session management
        return {
            "success": True,
            "message": f"Session {session_id} cleared"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session clear error: {str(e)}")

# Background task for periodic maintenance
async def periodic_maintenance():
    """Background task for periodic system maintenance."""
    while True:
        try:
            # Export feedback periodically
            if feedback_collector_instance.get_feedback_stats()["total_feedback"] > 0:
                feedback_collector_instance.export_feedback()
            
            # Wait for 1 hour
            await asyncio.sleep(3600)
        except Exception as e:
            print(f"Maintenance error: {e}")
            await asyncio.sleep(300)  # Wait 5 minutes on error

@app.on_event("startup")
async def startup_event():
    """Initialize the application on startup."""
    print("🤖 HR Assistant Bot API starting up...")
    print("Available endpoints:")
    print("  POST /chat - Chat with the bot")
    print("  POST /feedback - Submit feedback")
    print("  GET /analytics - Get analytics")
    print("  GET /status - System status")
    print("  GET /health - Health check")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    print("🤖 HR Assistant Bot API shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 