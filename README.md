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

## Technical Documentation

### Agent Architecture

The main agent (`agents/basic_agent.py`) uses LangChain's conversational agent pattern:

1. **LLM Initialization**: GPT-4 with temperature 0 for consistent responses
2. **Memory Management**: ConversationBufferMemory for context retention
3. **Tool Integration**: Custom tools for HR-specific functions
4. **Knowledge Base**: LlamaIndex-based semantic search over HR documents
5. **Escalation Logic**: Multi-criteria escalation system

### Document Processing

The document parser (`data_ingest/document_parser.py`) supports:

- **File Formats**: PDF, DOCX, TXT, MD
- **Parser**: UnstructuredReader for consistent extraction
- **Metadata**: File source, type, and size tracking
- **Error Handling**: Graceful failure handling with logging

### Escalation System

The escalation logic (`agents/escalation.py`) triggers based on:

1. **Low Confidence**: Confidence score below threshold
2. **User Requests**: Direct requests for human assistance
3. **Repeated Failures**: Multiple fallback responses
4. **Sensitive Topics**: Keywords indicating HR intervention needed
5. **Negative Sentiment**: User frustration detection
6. **Form Failures**: Repeated form completion issues
7. **Loop Detection**: Repeated similar intents

### Feedback System

The feedback collector tracks:

- **Session Data**: User queries, bot responses, session IDs
- **Performance Metrics**: Response times, tool usage
- **User Ratings**: 1-5 scale with optional text feedback
- **Escalation Events**: When and why escalations occur
- **Analytics**: Statistical analysis of bot performance

### Memory Management

The memory system provides:

- **Conversation History**: Full chat history retention
- **Session Tracking**: Unique session IDs for analytics
- **Context Preservation**: Maintains conversation context across turns

### Testing Framework

The testing suite includes:

1. **Unit Tests** (`test_unit.py`): Individual component testing
2. **Integration Tests** (`test_integration.py`): Component interaction testing
3. **End-to-End Tests** (`test_e2e.py`): Full workflow testing
4. **Test Runner** (`run_all_tests.py`): Comprehensive test execution

## Testing

### Running Tests

```bash
# Run all tests
python tests/run_all_tests.py

# Run specific test files
pytest tests/test_unit.py
pytest tests/test_integration.py
pytest tests/test_e2e.py
```

### Test Coverage

- **Unit Tests**: Agent logic, document parsing, escalation
- **Integration Tests**: API endpoints, tool interactions
- **End-to-End Tests**: Complete user workflows
- **Performance Tests**: Response time and memory usage

## Deployment

### Development Deployment

1. **Local Development**
   ```bash
   # Start all services
   uvicorn api.main:app --reload --port 8000 &
   streamlit run ui/streamlit_app.py --server.port 8501 &
   ```

2. **Docker Deployment**
   ```dockerfile
   FROM python:3.9-slim
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   COPY . .
   CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

### Production Considerations

1. **Environment Variables**: Secure API key management
2. **Database**: Consider PostgreSQL for production
3. **Caching**: Redis for session management
4. **Monitoring**: Application performance monitoring
5. **Security**: HTTPS, CORS configuration, rate limiting

### Configuration

Key configuration options:

- **OpenAI Model**: Change model in `agents/basic_agent.py`
- **Escalation Thresholds**: Adjust in `agents/escalation.py`
- **API Rate Limits**: Configure in `api/main.py`
- **UI Customization**: Modify `ui/streamlit_app.py`

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure virtual environment is activated
2. **API Key Issues**: Verify `.env` file configuration
3. **Document Parsing**: Check file format support
4. **Memory Issues**: Monitor conversation history size
5. **Performance**: Optimize response time with caching

### Logs and Debugging

- **Application Logs**: Check console output for errors
- **Escalation Logs**: Review `escalation_log.txt`
- **Feedback Data**: Inspect SQLite database
- **API Logs**: FastAPI automatic logging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the API documentation 