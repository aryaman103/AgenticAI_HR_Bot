# HR Agentic Bot

An intelligent HR assistant bot built with LangChain, OpenAI, and modern web technologies. The bot provides automated HR support with document parsing, escalation handling, and comprehensive feedback collection.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Technical Documentation](#technical-documentation)
- [Testing](#testing)
- [Deployment](#deployment)

## Features

- **Intelligent HR Support**: Automated responses to HR queries using GPT-4
- **Document Parsing**: Support for PDF, DOCX, TXT files with semantic search
- **Escalation System**: Smart escalation to human HR when needed
- **Multi-Interface**: Command-line, Streamlit web app, and REST API
- **Feedback Collection**: Comprehensive feedback system with analytics
- **Memory Management**: Conversation memory and session tracking
- **Error Handling**: Robust error handling and logging

## Architecture

### Core Components

```
hr-agentic-bot/
├── agents/                 # Core agent logic
│   ├── basic_agent.py     # Main agent implementation
│   ├── escalation.py      # Escalation logic
│   └── tools.py           # Agent tools
├── api/                   # FastAPI backend
│   └── main.py           # REST API endpoints
├── ui/                    # User interfaces
│   ├── streamlit_app.py  # Streamlit web interface
│   └── index.html        # HTML/JS frontend
├── data_ingest/          # Document processing
│   ├── document_parser.py # Document parsing logic
│   └── ingest.py         # Knowledge base building
├── memory/               # Memory management
│   └── memory.py         # Memory utilities
├── tests/                # Test suite
│   ├── test_unit.py      # Unit tests
│   ├── test_integration.py # Integration tests
│   └── test_e2e.py      # End-to-end tests
└── feedback/             # Feedback system
    └── feedback_collector.py # Feedback collection
```

### Technology Stack

- **Backend**: Python 3.8+, FastAPI, LangChain, OpenAI
- **Frontend**: Streamlit, HTML/JavaScript
- **Database**: SQLite (for feedback storage)
- **Document Processing**: LlamaIndex, Unstructured
- **Testing**: pytest, pytest-asyncio
- **Development**: Black, flake8, mypy

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hr-agentic-bot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```bash
   OPENAI_API_KEY=your_openai_api_key_here
   ```

5. **Prepare HR documents**
   Place your HR documents (PDF, DOCX, TXT) in the `data_ingest/` directory.

### Quick Start

1. **Command Line Interface**
   ```bash
   python agents/basic_agent.py
   ```

2. **Streamlit Web Interface**
   ```bash
   streamlit run ui/streamlit_app.py
   ```

3. **FastAPI Backend**
   ```bash
   uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Run Tests**
   ```bash
   python tests/run_all_tests.py
   ```

## Usage

### Command Line Interface

The CLI provides an interactive chat interface with feedback collection:

```bash
python agents/basic_agent.py
```

Features:
- Interactive chat with the HR bot
- Automatic feedback collection
- Session tracking
- Statistics display (`stats` command)

### Web Interface (Streamlit)

Access the modern web interface:

```bash
streamlit run ui/streamlit_app.py
```

Features:
- Real-time chat interface
- Feedback collection with ratings
- Analytics dashboard
- Admin panel

### REST API

Start the FastAPI server:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

API endpoints:
- `POST /chat` - Send messages to the bot
- `POST /feedback` - Submit feedback
- `GET /analytics` - Get analytics data
- `GET /status` - System status
- `GET /health` - Health check

## API Documentation

### Chat Endpoint

```http
POST /chat
Content-Type: application/json

{
  "message": "What is the leave policy?",
  "session_id": "optional_session_id",
  "user_id": "optional_user_id"
}
```

Response:
```json
{
  "response": "Based on our HR policies...",
  "session_id": "abc123",
  "response_time": 1.23,
  "escalation_triggered": false,
  "tools_used": ["KnowledgeBase"],
  "confidence": 0.85
}
```

### Feedback Endpoint

```http
POST /feedback
Content-Type: application/json

{
  "session_id": "abc123",
  "user_query": "What is the leave policy?",
  "bot_response": "Based on our HR policies...",
  "rating": 5,
  "feedback_text": "Very helpful response",
  "tools_used": ["KnowledgeBase"],
  "response_time": 1.23,
  "escalation_triggered": false
}
```

### Analytics Endpoint

```http
GET /analytics
```

Response:
```json
{
  "total_feedback": 150,
  "average_rating": 4.2,
  "escalation_rate": 0.05,
  "average_response_time": 1.45,
  "rating_distribution": {
    "1": 5,
    "2": 10,
    "3": 25,
    "4": 60,
    "5": 50
  },
  "recent_feedback": [...]
}
```
