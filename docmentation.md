# Gemma Chatbot API 🤖

A conversational chatbot API powered by Google's Gemma-3-1B-IT model, built with FastAPI.

## 📋 Project Status

### ✅ Completed (Person 1 - Backend Core)

**Files Created:**
- ✅ `backend/main.py` - FastAPI application setup
- ✅ `backend/config.py` - Configuration management
- ✅ `backend/api/routes.py` - All API endpoints
- ✅ `backend/models/schemas.py` - Request/Response models
- ✅ `backend/utils/helpers.py` - Utility functions
- ✅ `backend/__init__.py` - Package initialization
- ✅ `requirements.txt` - Python dependencies

**Features Implemented:**
- ✅ FastAPI application with CORS
- ✅ Health check endpoint (`GET /api/v1/health`)
- ✅ Chat endpoint (`POST /api/v1/chat`)
- ✅ Session management endpoints:
  - `GET /api/v1/sessions` - List all sessions
  - `GET /api/v1/sessions/{id}/info` - Get session info
  - `DELETE /api/v1/sessions/{id}` - Delete session
  - `POST /api/v1/sessions/{id}/clear-history` - Clear history
- ✅ Request/response validation with Pydantic
- ✅ Comprehensive error handling
- ✅ Logging infrastructure
- ✅ API documentation (Swagger/ReDoc)

### 🚧 TODO (Person 2 - Chat Service & Model)

**Files to Create:**
- ⏳ `backend/services/chat_service.py` - Main chat logic
- ⏳ `backend/services/__init__.py` - Services package

**Tasks:**
1. **Model Integration:**
   - Load `google/gemma-3-1b-it` model (HuggingFace or Ollama)
   - Set up tokenizer and generation pipeline
   - Configure model parameters (temperature, max_tokens, etc.)

2. **Chat Service Implementation:**
   - Implement `ChatService` class
   - Handle conversation history with LangChain
   - Create prompt templates
   - Implement `chat()` method for generating responses
   - Implement session management methods:
     - `get_session_history()`
     - `clear_history()`
     - `delete_session()`
     - `get_message_count()`
     - `session_exists()`
     - `is_model_loaded()`
     - `get_active_sessions_count()`
     - `get_all_sessions()`
     - `get_session_created_time()`

3. **Testing:**
   - Test model loading and inference
   - Test conversation flow
   - Optimize response quality

### 🎨 TODO (Person 3 - Frontend & Testing)

**Files to Create:**
- ⏳ `frontend/index.html` - Chat interface
- ⏳ `frontend/app.js` - Frontend logic
- ⏳ `frontend/styles.css` - Styling
- ⏳ `tests/test_api.py` - API tests
- ⏳ `tests/test_chat.py` - Chat functionality tests

**Tasks:**
1. **Frontend:**
   - Create simple chat interface
   - Implement message sending/receiving
   - Display conversation history
   - Add session management UI

2. **Testing:**
   - Write unit tests for API endpoints
   - Write integration tests
   - Test edge cases and error handling

3. **Documentation:**
   - Add API usage examples
   - Create user guide
   - Document deployment process

---

## 🚀 Quick Start (Current State)

### Prerequisites
```bash
# Python 3.9+
python --version

# Virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Installation
```bash
# Install dependencies
pip install -r requirements.txt
```

### Configuration
Create a `.env` file in the project root:
```env
# API Settings
API_TITLE=Gemma Chatbot API
API_VERSION=1.0.0

# Model Settings
MODEL_NAME=google/gemma-3-1b-it
MODEL_DEVICE=cpu
TEMPERATURE=0.7
MAX_TOKENS=512

# Optional: HuggingFace Token
HUGGINGFACE_TOKEN=your_token_here
```

### Running the API (After Person 2 completes chat_service.py)
```bash
# Development mode
python -m backend.main

# Or using uvicorn directly
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### Access
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/api/v1/health

---

## 📁 Project Structure

```
defi-project/
├── backend/
│   ├── __init__.py                 ✅ Done
│   ├── main.py                     ✅ Done
│   ├── config.py                   ✅ Done
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py               ✅ Done
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py              ✅ Done
│   ├── services/
│   │   ├── __init__.py             ⏳ Person 2
│   │   └── chat_service.py         ⏳ Person 2
│   └── utils/
│       ├── __init__.py
│       └── helpers.py              ✅ Done
├── frontend/                       ⏳ Person 3
│   ├── index.html
│   ├── app.js
│   └── styles.css
├── tests/                          ⏳ Person 3
│   ├── test_api.py
│   └── test_chat.py
├── requirements.txt                ✅ Done
├── .env                            ⏳ Create this
└── README.md                       ✅ Done
```

---

## 🧪 Testing Current Implementation

### Test 1: Health Check
```bash
curl http://localhost:8000/api/v1/health
```

**Expected Response (will show error until Person 2 completes chat_service):**
```json
{
  "status": "unhealthy",
  "error": "chat_service not initialized",
  "note": "Person 2 needs to implement chat_service.py"
}
```

### Test 2: Root Endpoint
```bash
curl http://localhost:8000/
```

**Expected Response:**
```json
{
  "message": "Welcome to Gemma Chatbot API",
  "version": "1.0.0",
  "model": "google/gemma-3-1b-it",
  "docs": "/docs",
  "health": "/api/v1/health"
}
```

### Test 3: API Documentation
Open browser: `http://localhost:8000/docs`

You should see:
- All endpoints documented
- Interactive API testing interface
- Request/response schemas

---

## 📝 API Endpoints

### Chat
- **POST** `/api/v1/chat` - Send message and get response

### Sessions
- **GET** `/api/v1/sessions` - List all sessions
- **GET** `/api/v1/sessions/{id}/info` - Get session details
- **DELETE** `/api/v1/sessions/{id}` - Delete session
- **POST** `/api/v1/sessions/{id}/clear-history` - Clear chat history

### System
- **GET** `/api/v1/health` - Health check
- **GET** `/` - Root info

---

## 🤝 Team Workflow

### Person 1 (You) - ✅ COMPLETED
Your work is done! The API infrastructure is ready.

### Person 2 - Next Steps
1. Clone the repo and pull Person 1's code
2. Create `backend/services/chat_service.py`
3. Implement model loading (HuggingFace or Ollama)
4. Implement ChatService class with all required methods
5. Test with API endpoints
6. Push code for Person 3

### Person 3 - After Person 2
1. Pull Person 2's code
2. Create simple frontend to test chatbot
3. Write comprehensive tests
4. Document everything
5. Prepare for deployment

---

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MODEL_NAME` | `google/gemma-3-1b-it` | Model identifier |
| `MODEL_DEVICE` | `cpu` | Device: `cpu` or `cuda` |
| `TEMPERATURE` | `0.7` | Response randomness (0-1) |
| `MAX_TOKENS` | `512` | Max response length |
| `MAX_HISTORY_LENGTH` | `10` | Conversation history limit |

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gemma Model Card](https://huggingface.co/google/gemma-3-1b-it)
- [LangChain Docs](https://python.langchain.com/)
- [Pydantic Docs](https://docs.pydantic.dev/)

---

## 🐛 Known Issues

- ⚠️ Chat endpoint will return 500 error until `chat_service.py` is implemented
- ⚠️ Health check will show "unhealthy" until model is loaded

---

## 📄 License

MIT License - feel free to use this project for learning and development.

---

**Status**: Person 1 work complete ✅ | Waiting for Person 2 to implement chat service 🚧