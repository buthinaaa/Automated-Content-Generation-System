"""
STUB Chat Service for Person 1 Testing
Person 2: Replace this entire file with actual implementation
"""
from typing import Dict, List
import logging
from datetime import datetime

from langchain_community.chat_message_histories import ChatMessageHistory

logger = logging.getLogger(__name__)


class ChatService:
    """
    STUB ChatService - Minimal implementation for testing Person 1's work
    Person 2 should replace this with full implementation including:
    - Actual model loading (HuggingFace/Ollama)
    - Real inference logic
    - Proper prompt engineering
    """
    
    def __init__(self):
        """Initialize stub chat service"""
        self.session_store: Dict[str, ChatMessageHistory] = {}
        self.session_created: Dict[str, str] = {}
        self.model_loaded = False
        logger.warning("⚠️  Using STUB ChatService - Person 2 needs to implement this!")
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded (stub always returns False)"""
        return self.model_loaded
    
    def get_session_history(self, session_id: str) -> ChatMessageHistory:
        """Get or create chat history for session"""
        if session_id not in self.session_store:
            self.session_store[session_id] = ChatMessageHistory()
            self.session_created[session_id] = datetime.now().isoformat()
            logger.info(f"Created new session: {session_id}")
        return self.session_store[session_id]
    
    async def chat(self, prompt: str, session_id: str) -> str:
        """
        STUB chat implementation - returns placeholder response
        Person 2: Replace with actual model inference
        """
        # Get/create session
        history = self.get_session_history(session_id)
        
        # Add user message to history
        history.add_user_message(prompt)
        
        # STUB response (Person 2 replace this with model inference)
        stub_response = (
            f"[STUB RESPONSE] This is a placeholder. "
            f"Person 2 needs to implement actual model inference. "
            f"You said: '{prompt[:50]}...'"
        )
        
        # Add AI response to history
        history.add_ai_message(stub_response)
        
        logger.warning(f"⚠️  Returning stub response for session {session_id}")
        
        return stub_response
    
    def clear_history(self, session_id: str) -> None:
        """Clear chat history for session"""
        if session_id in self.session_store:
            self.session_store[session_id] = ChatMessageHistory()
            logger.info(f"Cleared history for session {session_id}")
    
    def delete_session(self, session_id: str) -> None:
        """Delete session"""
        if session_id in self.session_store:
            del self.session_store[session_id]
            if session_id in self.session_created:
                del self.session_created[session_id]
            logger.info(f"Deleted session {session_id}")
    
    def get_message_count(self, session_id: str) -> int:
        """Get number of messages in session"""
        if session_id not in self.session_store:
            return 0
        return len(self.session_store[session_id].messages)
    
    def session_exists(self, session_id: str) -> bool:
        """Check if session exists"""
        return session_id in self.session_store
    
    def get_active_sessions_count(self) -> int:
        """Get count of active sessions"""
        return len(self.session_store)
    
    def get_all_sessions(self) -> List[Dict]:
        """Get all active sessions with info"""
        sessions = []
        for session_id in self.session_store.keys():
            sessions.append({
                "session_id": session_id,
                "message_count": self.get_message_count(session_id)
            })
        return sessions
    
    def get_session_created_time(self, session_id: str) -> str:
        """Get session creation time"""
        return self.session_created.get(session_id, datetime.now().isoformat())


# Global instance
chat_service = ChatService()