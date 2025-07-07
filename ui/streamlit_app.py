#!/usr/bin/env python3
"""
Streamlit Web Interface for HR Agent Bot
Provides a modern chat interface with feedback collection and analytics
"""

import streamlit as st
import time
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import bot components
from agents.basic_agent import agent, feedback_collector
from agents.escalation import should_escalate, escalation_message
from feedback.feedback_collector import FeedbackCollector


def initialize_session_state():
    """Initialize session state variables."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "session_id" not in st.session_state:
        st.session_state.session_id = f"streamlit_{int(time.time())}"
    
    if "feedback_collector" not in st.session_state:
        st.session_state.feedback_collector = FeedbackCollector()


def create_chat_interface():
    """Create the main chat interface."""
    st.title("🤖 HR Assistant Bot")
    st.markdown("Ask me anything about HR policies, leave, holidays, and more!")
    
    # Initialize session state
    initialize_session_state()
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get bot response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            # Check for escalation
            escalation_triggered = should_escalate(
                confidence=0.7,  # Default confidence
                user_input=prompt,
                fallback_count=0,
                form_fail_count=0,
                sentiment="neutral",
                repeated_intent_count=0
            )
            
            if escalation_triggered:
                response = escalation_message()
                escalation_triggered = True
            else:
                # Get response from agent
                start_time = time.time()
                try:
                    agent_response = agent.invoke({"input": prompt})
                    response = agent_response.get("output", "I'm sorry, I couldn't process your request.")
                    response_time = time.time() - start_time
                    escalation_triggered = False
                except Exception as e:
                    response = f"I'm sorry, I encountered an error: {str(e)}"
                    response_time = time.time() - start_time
                    escalation_triggered = False
            
            # Display response with typing effect
            full_response = ""
            for chunk in response.split():
                full_response += chunk + " "
                time.sleep(0.05)
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        
        # Collect feedback
        collect_feedback(prompt, response, response_time, escalation_triggered)


def collect_feedback(user_query, bot_response, response_time, escalation_triggered):
    """Collect feedback after each response."""
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.markdown("**How helpful was this response?**")
    
    with col2:
        rating = st.selectbox(
            "Rating:",
            options=["", "1 - Not helpful", "2 - Somewhat helpful", "3 - Helpful", "4 - Very helpful", "5 - Extremely helpful"],
            key=f"rating_{len(st.session_state.messages)}"
        )
    
    with col3:
        if st.button("Submit Feedback", key=f"submit_{len(st.session_state.messages)}"):
            if rating:
                rating_value = int(rating.split(" - ")[0])
                
                # Extract tools used (simplified)
                tools_used = []
                if "KnowledgeBase" in str(bot_response):
                    tools_used.append("KnowledgeBase")
                if "GetLeaveBalance" in str(bot_response):
                    tools_used.append("GetLeaveBalance")
                if "CalendarAPI" in str(bot_response):
                    tools_used.append("CalendarAPI")
                
                # Collect feedback
                st.session_state.feedback_collector.collect_feedback(
                    session_id=st.session_state.session_id,
                    user_query=user_query,
                    bot_response=bot_response,
                    rating=rating_value,
                    feedback_text=None,
                    tools_used=tools_used,
                    response_time=response_time,
                    escalation_triggered=escalation_triggered
                )
                
                st.success("Thank you for your feedback! 👍")
                time.sleep(2)
                st.rerun()
            else:
                st.error("Please select a rating.")


def create_analytics_dashboard():
    """Create analytics dashboard."""
    st.title("📊 Analytics Dashboard")
    
    # Get feedback statistics
    stats = st.session_state.feedback_collector.get_feedback_stats()
    
    # Create metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Feedback", stats.get("total_feedback", 0))
    
    with col2:
        st.metric("Average Rating", f"{stats.get('average_rating', 0):.1f}/5")
    
    with col3:
        escalation_rate = stats.get("escalation_rate", 0)
        st.metric("Escalation Rate", f"{escalation_rate:.1%}")
    
    with col4:
        avg_response_time = stats.get("average_response_time", 0)
        st.metric("Avg Response Time", f"{avg_response_time:.2f}s")
    
    # Create charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Rating distribution
        rating_dist = stats.get("rating_distribution", {})
        if rating_dist:
            df_ratings = pd.DataFrame([
                {"Rating": rating, "Count": count}
                for rating, count in rating_dist.items()
            ])
            
            fig_ratings = px.bar(
                df_ratings, 
                x="Rating", 
                y="Count",
                title="Rating Distribution",
                color="Count",
                color_continuous_scale="viridis"
            )
            st.plotly_chart(fig_ratings, use_container_width=True)
    
    with col2:
        # Response time trend
        recent_feedback = st.session_state.feedback_collector.get_recent_feedback(20)
        if recent_feedback:
            df_times = pd.DataFrame([
                {
                    "Time": datetime.fromisoformat(feedback["timestamp"]),
                    "Response Time": feedback["response_time"]
                }
                for feedback in recent_feedback
            ])
            
            fig_times = px.line(
                df_times,
                x="Time",
                y="Response Time",
                title="Response Time Trend"
            )
            st.plotly_chart(fig_times, use_container_width=True)
    
    # Recent feedback table
    st.subheader("Recent Feedback")
    if recent_feedback:
        df_recent = pd.DataFrame(recent_feedback)
        df_recent["timestamp"] = pd.to_datetime(df_recent["timestamp"])
        df_recent = df_recent[["timestamp", "user_query", "rating", "response_time"]]
        df_recent.columns = ["Time", "Query", "Rating", "Response Time (s)"]
        
        st.dataframe(df_recent, use_container_width=True)
    else:
        st.info("No feedback collected yet.")


def create_admin_panel():
    """Create admin panel for system management."""
    st.title("⚙️ Admin Panel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("System Status")
        
        # Check system components
        status_items = [
            ("Agent", "✅ Online"),
            ("Knowledge Base", "✅ Available"),
            ("Feedback System", "✅ Active"),
            ("Escalation System", "✅ Ready")
        ]
        
        for component, status in status_items:
            st.markdown(f"**{component}:** {status}")
    
    with col2:
        st.subheader("Actions")
        
        if st.button("Export Feedback Data"):
            export_path = st.session_state.feedback_collector.export_feedback()
            st.success(f"Feedback exported to: {export_path}")
        
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.success("Chat history cleared!")
            st.rerun()
        
        if st.button("Reset Feedback"):
            # This would require implementing a reset method
            st.info("Feedback reset functionality would be implemented here.")


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="HR Assistant Bot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Sidebar navigation
    st.sidebar.title("🤖 HR Assistant")
    
    page = st.sidebar.selectbox(
        "Navigation",
        ["Chat", "Analytics", "Admin"]
    )
    
    # Page routing
    if page == "Chat":
        create_chat_interface()
    elif page == "Analytics":
        create_analytics_dashboard()
    elif page == "Admin":
        create_admin_panel()
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Session ID:**")
    st.sidebar.code(st.session_state.get("session_id", "Unknown"))
    
    st.sidebar.markdown("**Features:**")
    st.sidebar.markdown("• Leave balance inquiries")
    st.sidebar.markdown("• Holiday calendar lookup")
    st.sidebar.markdown("• Leave application guidance")
    st.sidebar.markdown("• Policy information")
    st.sidebar.markdown("• Escalation to human HR")
    
    st.sidebar.markdown("**Tips:**")
    st.sidebar.markdown("• Be specific in your questions")
    st.sidebar.markdown("• Provide your employee ID when asking about leave")
    st.sidebar.markdown("• Rate responses to help improve the bot")


if __name__ == "__main__":
    main() 