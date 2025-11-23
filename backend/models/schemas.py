"""
Pydantic models for request and response validation
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    prompt: str = Field(
        ..., 
        min_length=1, 
        max_length=5000, 
        description="User's message/question"
    )
    session_id: str = Field(
        ..., 
        min_length=5, 
        description="Unique session identifier"
    )
    
    @validator('prompt')
    def prompt_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Prompt cannot be empty or whitespace')
        return v.strip()
    
    @validator('session_id')
    def validate_session_format(cls, v):
        # Allow flexible session ID format
        if not v or len(v) < 5:
            raise ValueError('Session ID must be at least 5 characters')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "prompt": "Hello! How are you?",
                "session_id": "session_12345"
            }
        }


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    answer: str = Field(..., description="AI generated answer")
    session_id: str = Field(..., description="Session identifier")
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Hello! I'm doing well, thank you for asking. How can I help you today?",
                "session_id": "session_12345"
            }
        }


class SessionInfo(BaseModel):
    """Session information response"""
    session_id: str
    message_count: int
    created_at: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "session_12345",
                "message_count": 10,
                "created_at": "2025-11-23T10:30:00"
            }
        }


class SessionListItem(BaseModel):
    """Individual session in list"""
    session_id: str
    message_count: int


class SessionListResponse(BaseModel):
    """Response for listing all sessions"""
    sessions: List[SessionListItem]
    count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "sessions": [
                    {"session_id": "session_12345", "message_count": 5},
                    {"session_id": "session_67890", "message_count": 12}
                ],
                "count": 2
            }
        }


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    model_name: str
    model_status: str
    active_sessions: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "model_name": "google/gemma-3-1b-it",
                "model_status": "connected",
                "active_sessions": 3
            }
        }


class MessageResponse(BaseModel):
    """Simple message response"""
    message: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Operation completed successfully"
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response"""
    detail: str
    error_type: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Session not found",
                "error_type": "NotFoundError"
            }
        }