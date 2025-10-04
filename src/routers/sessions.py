"""
AI Cyber Tool - Sessions Router
API ендпоінти для роботи з сесіями
"""

from fastapi import APIRouter, HTTPException
from loguru import logger
from ..models.session import SessionCreate, SessionResponse, AnalysisLogCreate
from ..db.database import get_sessions, create_session, create_analysis_log

router = APIRouter()


@router.get("/api/sessions")
async def get_sessions_endpoint():
    """Отримання списку всіх сесій (асинхронно)"""
    try:
        sessions = await get_sessions()
        return {"payload": sessions, "count": len(sessions)}
    except Exception as e:
        logger.error(f"Failed to get sessions: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve sessions")


@router.post("/api/sessions", response_model=SessionResponse)
async def create_session_endpoint(session: SessionCreate):
    """Створення нової сесії з валідацією"""
    try:
        session_data = await create_session(session.session_name)
        logger.info(f"Created new session: {session.session_name} (ID: {session_data[0]})")
        
        return SessionResponse(
            id=session_data[0],
            session_name=session_data[1],
            created_at=session_data[2],
            status=session_data[3]
        )
    except Exception as e:
        logger.error(f"Failed to create session: {e}")
        raise HTTPException(status_code=500, detail="Failed to create session")


@router.post("/api/analysis-logs")
async def create_analysis_log_endpoint(log: AnalysisLogCreate):
    """Створення нового логу аналізу з валідацією"""
    try:
        log_id = await create_analysis_log(log.session_id, log.log_type, log.message)
        logger.info(f"Created analysis log for session {log.session_id}: {log.log_type}")
        
        return {
            "id": log_id,
            "session_id": log.session_id,
            "log_type": log.log_type,
            "message": log.message,
            "message": "Analysis log created successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Failed to create analysis log: {e}")
        raise HTTPException(status_code=500, detail="Failed to create analysis log")
