# 🌍 World History Chatbot

A conversational AI chatbot specialized in world history, powered by a fine-tuned Qwen-2B model. Built as a final project for the DEPI course.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [API Endpoints](#api-endpoints)
- [Project Structure](#project-structure)
- [What We Built](#what-we-built)
- [Troubleshooting](#troubleshooting)
- [Technologies Used](#technologies-used)

---

## 🎯 Overview

This project is an intelligent chatbot that can answer questions about world history. The chatbot uses a fine-tuned Qwen 2B model trained on historical data, and provides accurate, contextual responses while maintaining conversation history across multiple turns.

**Model:** Fine-tuned version of `Qwen/Qwen2.5-1.5B-Instruct` on world history dataset  
**Deployment:** Local deployment with FastAPI backend and vanilla JavaScript frontend  
**Optimization:** 8-bit quantization for efficient CPU inference

---

## ✨ Features

- 💬 **Natural Conversations**: Ask questions about any historical period, event, or figure
- 🧠 **Context Awareness**: Maintains conversation history for follow-up questions
- 🔄 **Session Management**: Multiple independent chat sessions
- 🗑️ **History Control**: Clear conversation history or start fresh sessions
- ⚡ **CPU Optimized**: Runs on consumer hardware with 8-bit quantization
- 🌐 **Simple UI**: Clean, responsive web interface

---

## 📦 Prerequisites

### System Requirements:
- **OS**: Windows (tested), Linux/Mac should work
- **Python**: 3.10 or higher
- **RAM**: Minimum 12GB
- **Storage**: ~6GB free space for model files
- **CPU**: Modern multi-core processor (no GPU required)

### Software Requirements:
- Python 3.10+
- pip (Python package manager)
- Web browser (Chrome, Firefox, Edge, etc.)

---

## 🚀 Installation

### Step 1: Clone the Repository

```bash
git clone <your-repo-url>
cd DEFI-project
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Required packages include:**
- FastAPI & Uvicorn (API server)
- Transformers (Model loading)
- PyTorch (ML framework)
- bitsandbytes (8-bit quantization)
- LangChain (Conversation management)

### Step 4: Download the Fine-tuned Model

**IMPORTANT: Do this BEFORE starting the server!**

Create a Python script `download_model.py`:

```python
from huggingface_hub import snapshot_download

print("📥 Downloading model from HuggingFace...")
print("⏳ This will take 5-10 minutes (downloads ~3GB)...")

snapshot_download(
    repo_id="loaimo/qwen-world-history",
    local_dir="qwen-world-history"
)

print("✅ Model downloaded successfully!")
print("📁 Model saved to: ./qwen-world-history/")
```

Run it:

```bash
python download_model.py
```

**Expected folder structure after download:**
```
DEFI-project/
├── qwen-world-history/          ← Model files here
│   ├── config.json
│   ├── model.safetensors
│   ├── tokenizer.json
│   └── ...
├── backend/
├── frontend/
└── requirements.txt
```

### Step 5: Configure Environment

Create a `.env` file in the project root:

```bash
# Model Settings
MODEL_NAME=./qwen-world-history
MODEL_DEVICE=cpu

# Generation Parameters
TEMPERATURE=0.7
MAX_TOKENS=512
TOP_P=0.9

# Session Settings
MAX_HISTORY_LENGTH=10
```

---

## 🎮 Running the Project

You need to run **TWO servers** (backend and frontend) in **separate terminals**.

### Terminal 1: Start Backend Server

```bash
# Make sure virtual environment is activated
# Navigate to project root
cd DEFI-project

# Start FastAPI backend
python -m backend.main
```

**Expected output:**
```
✅ PyTorch and Transformers imported
✅ Config loaded: ./qwen-world-history
🚀 INITIALIZING CHAT SERVICE
✅ Model loaded successfully!
🎉 Global chat_service ready!
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Backend will be available at:** `http://localhost:8000`

---

### Terminal 2: Start Frontend Server

Open a **NEW terminal** (keep backend running):

```bash
# Navigate to frontend folder
cd DEFI-project/frontend

# Start simple HTTP server
python -m http.server 3000
```

**Expected output:**
```
Serving HTTP on 0.0.0.0 port 3000 (http://0.0.0.0:3000/) ...
```

**Frontend will be available at:** `http://localhost:3000`

---

### Access the Chatbot

Open your browser and go to:
```
http://localhost:3000
```

You should see the chat interface! 🎉

---

## 🔌 API Endpoints

The backend provides the following REST API endpoints:

### Health Check
```http
GET /api/v1/health
```
Check if the API and model are working.

**Response:**
```json
{
  "status": "healthy",
  "model_name": "./qwen-world-history",
  "model_status": "connected",
  "active_sessions": 2
}
```

---

### Chat
```http
POST /api/v1/chat
```
Send a message and get AI response.

**Request:**
```json
{
  "prompt": "Tell me about World War II",
  "session_id": "session_12345"
}
```

**Response:**
```json
{
  "answer": "World War II (1939-1945) was a global conflict...",
  "session_id": "session_12345"
}
```

---

### Get Session Info
```http
GET /api/v1/sessions/{session_id}/info
```
Get information about a specific session.

**Response:**
```json
{
  "session_id": "session_12345",
  "message_count": 8,
  "created_at": "2025-12-05T10:30:00"
}
```

---

### List All Sessions
```http
GET /api/v1/sessions
```
Get all active sessions.

**Response:**
```json
{
  "sessions": [
    {"session_id": "session_12345", "message_count": 8},
    {"session_id": "session_67890", "message_count": 3}
  ],
  "count": 2
}
```

---

### Clear Session History
```http
POST /api/v1/sessions/{session_id}/clear-history
```
Clear conversation history but keep the session.

**Response:**
```json
{
  "message": "Chat history cleared for session 'session_12345'"
}
```

---

### Delete Session
```http
DELETE /api/v1/sessions/{session_id}
```
Delete a session completely.

**Response:**
```json
{
  "message": "Session 'session_12345' deleted successfully"
}
```

---

## 📁 Project Structure

```
DEFI-project/
├── backend/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── config.py                  # Configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py              # API endpoint definitions
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py             # Pydantic request/response models
│   ├── services/
│   │   ├── __init__.py
│   │   └── chat_service.py        # Chat logic and model inference
│   └── utils/
│       ├── __init__.py
│       └── helpers.py             # Utility functions
├── frontend/
│   ├── index.html                 # Main HTML page
│   ├── app.js                     # Frontend JavaScript logic
│   └── styles.css                 # Styling
├── qwen-world-history/            # Fine-tuned model (downloaded)
│   ├── config.json
│   ├── model.safetensors
│   └── ...
├── requirements.txt               # Python dependencies
├── .env                          # Environment configuration
└── README.md                     # This file
```

---

## 🛠️ What We Built

### 1. Model Fine-tuning
- **Base Model**: Qwen/Qwen2.5-1.5B-Instruct (1.5 billion parameters)
- **Fine-tuning**: Trained on world history dataset from HuggingFace
- **Optimization**: 8-bit quantization for efficient CPU inference
- **Result**: Specialized chatbot for historical questions

### 2. Backend Development (FastAPI)
- **RESTful API**: 7 endpoints for chat and session management
- **Request Validation**: Pydantic models for type safety
- **Error Handling**: Comprehensive error messages and logging
- **Session Management**: In-memory storage for conversation history
- **Model Integration**: 8-bit quantized model loading with bitsandbytes

### 3. Frontend Development
- **Simple UI**: Clean, responsive chat interface
- **Real-time Chat**: Instant message sending and receiving
- **Session Control**: Clear history, manage multiple sessions
- **User Feedback**: Loading states, error messages, typing indicators

### 4. Key Technical Achievements
- ✅ Successfully loaded 1.5B parameter model on CPU
- ✅ Implemented 8-bit quantization for memory efficiency
- ✅ Built complete REST API with FastAPI
- ✅ Created conversation history management
- ✅ Deployed locally with simple frontend

---

## 🐛 Troubleshooting

### Problem: Model fails to load

**Error:** `Model loading failed` or `bitsandbytes error`

**Solution:**
```bash
# Make sure bitsandbytes is installed
pip install bitsandbytes accelerate

# Verify model files exist
ls qwen-world-history/
# Should show: config.json, model.safetensors, tokenizer files
```

---

### Problem: Backend won't start

**Error:** `Port 8000 already in use`

**Solution:**
```bash
# Kill process using port 8000
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or use different port:
uvicorn backend.main:app --port 8001
```

---

### Problem: Frontend can't connect to backend

**Error:** `Network error` or `Failed to fetch`

**Solution:**
1. Make sure backend is running (check Terminal 1)
2. Verify backend URL in `frontend/app.js` is `http://localhost:8000`
3. Check browser console for CORS errors

---

### Problem: Slow responses

**Cause:** CPU inference is slower than GPU

**Solutions:**
- ✅ Already using 8-bit quantization (fastest CPU option)
- ✅ Reduce `MAX_TOKENS` in `.env` to 256 or 128
- ✅ Close other applications to free RAM
- ✅ This is expected behavior on CPU

---

### Problem: Out of memory

**Error:** `RuntimeError: out of memory`

**Solution:**
```bash
# Close other applications
# Reduce max tokens in .env:
MAX_TOKENS=256

# Make sure you have 12GB+ RAM available
```

---

## 💻 Technologies Used

### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Transformers** - HuggingFace model loading
- **PyTorch** - Deep learning framework
- **bitsandbytes** - 8-bit quantization
- **LangChain** - Conversation history management
- **Pydantic** - Data validation

### Frontend
- **HTML5** - Structure
- **CSS3** - Styling
- **JavaScript (Vanilla)** - Logic and API calls
- **Fetch API** - HTTP requests

### Model
- **Qwen2.5-1.5B-Instruct** - Base model
- **Fine-tuned** on world history dataset
- **8-bit quantization** for CPU efficiency

---

## 🎓 Learning Outcomes

This project demonstrates:
- ✅ Fine-tuning large language models
- ✅ Building REST APIs with FastAPI
- ✅ Model optimization (quantization)
- ✅ Frontend-backend integration
- ✅ Session management and state handling
- ✅ Deploying ML models locally
- ✅ Working with HuggingFace ecosystem

---

## 📝 Notes

- **First startup** takes 1-2 minutes to load the model
- **Subsequent starts** are faster (~30 seconds)
- **CPU inference** is slower than GPU but works well for this use case
- **Memory usage** is ~4-6GB with 8-bit quantization
- Model responses may take **5-15 seconds** on CPU

---

## 🚀 Future Improvements

Potential enhancements:
- [ ] Add authentication and user accounts
- [ ] Persistent storage (database for sessions)
- [ ] Streaming responses (word-by-word generation)
- [ ] Better error messages in UI
- [ ] Mobile-responsive design improvements
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Add citation system (show sources)
- [ ] Multi-language support

---

## 📄 License

This project is for educational purposes as part of the DEPI course.

---

## 🙏 Acknowledgments

- **DEPI Course** - For the learning opportunity
- **HuggingFace** - For the model and dataset hosting
- **Qwen Team** - For the excellent base model
- **FastAPI Team** - For the amazing framework

---

## 📞 Support

If you encounter issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Verify all prerequisites are met
3. Check that both servers are running
4. Look at backend logs for detailed error messages

---

**Built with ❤️ for the DEPI Final Project**

*Last Updated: December 2025*
