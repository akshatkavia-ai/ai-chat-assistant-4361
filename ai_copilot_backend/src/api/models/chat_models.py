from pydantic import BaseModel, Field
from typing import Optional

# PUBLIC_INTERFACE
class ChatRequest(BaseModel):
    """Request model for chat messages.
    
    Attributes:
        message: The user's message to send to the AI copilot
    """
    message: str = Field(..., min_length=1, description='User message to the AI')

# PUBLIC_INTERFACE
class ChatResponse(BaseModel):
    """Response model for chat messages.
    
    Attributes:
        reply: The AI's response to the user's message
        error: Optional error message if something went wrong
    """
    reply: str
    error: Optional[str] = None
