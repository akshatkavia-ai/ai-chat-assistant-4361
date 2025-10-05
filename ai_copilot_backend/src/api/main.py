from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models.chat_models import ChatRequest, ChatResponse
from .services.gemini_service import GeminiClient
import os

app = FastAPI(
    title='AI Copilot Backend',
    description='Backend API for AI Copilot chat application with Gemini integration',
    version='1.0.0'
)

# CORS: allow frontend on 3000 and localhost variations
frontend_origin_env = os.getenv('FRONTEND_ORIGIN')
allowed_origins = [
    'http://localhost:3000',
    'http://127.0.0.1:3000'
]
if frontend_origin_env:
    allowed_origins.append(frontend_origin_env)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# PUBLIC_INTERFACE
@app.get('/', tags=['health'])
async def health():
    """Health check endpoint.
    
    Returns:
        dict: Status indicating the service is operational
    """
    return {'status': 'ok'}

# PUBLIC_INTERFACE
@app.post('/api/chat', response_model=ChatResponse, tags=['chat'], 
          summary='Send a chat message to the AI',
          description='Processes user messages and returns AI-generated responses using Gemini API')
async def chat(req: ChatRequest):
    """Process a chat message and return AI response.
    
    Args:
        req: ChatRequest containing the user's message
        
    Returns:
        ChatResponse with the AI's reply or error message
        
    Raises:
        HTTPException: 400 for configuration errors, 500 for unexpected errors
    """
    client = GeminiClient()
    try:
        reply = client.chat(req.message)
        if not reply:
            return ChatResponse(reply='', error='Empty response from model')
        return ChatResponse(reply=reply)
    except RuntimeError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Unexpected error: {str(e)}')
