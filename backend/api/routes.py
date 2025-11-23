"""
API routes for the Gemma Chatbot
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

from ..models.schemas import (
    ChatRequest, 
    ChatResponse, 
    SessionInfo, 
    HealthResponse,
    SessionListResponse,
    MessageResponse
)
from ..services.chat_service import chat_service
from ..config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Check if the API and model are working
    """
    try:
        # Test if chat service is initialized
        model_status = "connected" if chat_service.is_model_loaded() else "disconnected"
        
        return HealthResponse(
            status="healthy",
            model_name=settings.MODEL_NAME,
            model_status=model_status,
            active_sessions=chat_service.get_active_sessions_count()
        )
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "note": "Make sure the model is properly loaded"
            }
        )


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint for conversational AI
    """
    logger.info(f"💬 Received chat request for session: {request.session_id}")
    logger.info(f"📝 Prompt: {request.prompt[:100]}...")
    
    try:
        # Process chat
        answer = await chat_service.chat(request.prompt, request.session_id)
        
        logger.info(f"✅ Response generated for session {request.session_id}")
        
        return ChatResponse(
            answer=answer,
            session_id=request.session_id
        )
        
    except ValueError as e:
        logger.error(f"❌ Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Error generating response: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate response: {str(e)}"
        )


@router.get("/sessions/{session_id}/info", response_model=SessionInfo)
async def get_session_info(session_id: str):
    """
    Get information about a session
    """
    if not chat_service.session_exists(session_id):
        raise HTTPException(
            status_code=404, 
            detail=f"Session '{session_id}' not found"
        )
    
    return SessionInfo(
        session_id=session_id,
        message_count=chat_service.get_message_count(session_id),
        created_at=chat_service.get_session_created_time(session_id)
    )


@router.delete("/sessions/{session_id}", response_model=MessageResponse)
async def delete_session(session_id: str):
    """
    Delete a session and its chat history
    """
    try:
        if not chat_service.session_exists(session_id):
            raise HTTPException(
                status_code=404,
                detail=f"Session '{session_id}' not found"
            )
        
        chat_service.delete_session(session_id)
        logger.info(f"✅ Deleted session {session_id}")
        
        return MessageResponse(
            message=f"Session '{session_id}' deleted successfully"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting session: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete session: {str(e)}"
        )


@router.post("/sessions/{session_id}/clear-history", response_model=MessageResponse)
async def clear_session_history(session_id: str):
    """
    Clear chat history for a session
    """
    if not chat_service.session_exists(session_id):
        raise HTTPException(
            status_code=404, 
            detail=f"Session '{session_id}' not found"
        )
    
    chat_service.clear_history(session_id)
    logger.info(f"✅ Cleared history for session {session_id}")
    
    return MessageResponse(
        message=f"Chat history cleared for session '{session_id}'"
    )


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions():
    """
    List all active sessions
    """
    sessions = chat_service.get_all_sessions()
    
    return SessionListResponse(
        sessions=sessions,
        count=len(sessions)
    )