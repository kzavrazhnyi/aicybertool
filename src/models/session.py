"""
AI Cyber Tool - Session Models
Pydantic моделі для валідації даних сесій
"""

from pydantic import BaseModel, constr, validator


class SessionCreate(BaseModel):
    """Модель для створення нової сесії"""
    session_name: constr(min_length=1, max_length=100, strip_whitespace=True)
    
    @validator('session_name')
    def validate_session_name(cls, v):
        """Додаткова валідація назви сесії"""
        if not v or v.isspace():
            raise ValueError('Session name cannot be empty or whitespace only')
        
        # Перевірка на небезпечні символи
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '|', '`', '$']
        if any(char in v for char in dangerous_chars):
            raise ValueError('Session name contains potentially dangerous characters')
        
        return v


class SessionResponse(BaseModel):
    """Модель відповіді для сесії"""
    id: int
    session_name: str
    created_at: str
    status: str


class AnalysisLogCreate(BaseModel):
    """Модель для створення логу аналізу"""
    session_id: int
    log_type: constr(min_length=1, max_length=50)
    message: constr(min_length=1, max_length=1000)
