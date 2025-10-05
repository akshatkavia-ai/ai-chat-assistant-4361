import os
from typing import Optional

try:
    import google.generativeai as genai
except Exception:
    genai = None

GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

class GeminiClient:
    """Client for interacting with Google's Gemini AI API.
    
    This client manages the connection to the Gemini API and handles
    chat message generation with proper error handling.
    """
    
    def __init__(self):
        """Initialize the Gemini client with API key from environment.
        
        Note: Requires GEMINI_API_KEY environment variable to be set.
        """
        self.api_key = os.getenv('GEMINI_API_KEY')
        if genai and self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(GEMINI_MODEL)
        else:
            self.model = None

    # PUBLIC_INTERFACE
    def chat(self, prompt: str) -> Optional[str]:
        """Send a message to Gemini and get a response.
        
        Args:
            prompt: The user's message to send to the AI
            
        Returns:
            The AI's response text, or None if generation failed
            
        Raises:
            RuntimeError: If API key is missing, package unavailable, or API error occurs
        """
        if not self.api_key:
            raise RuntimeError('Missing GEMINI_API_KEY environment variable')
        if not genai or not self.model:
            raise RuntimeError('google-generativeai package not available or model not initialized')
        try:
            resp = self.model.generate_content(prompt)
            # Handle different SDK response structures defensively
            if hasattr(resp, 'text') and resp.text:
                return resp.text
            if hasattr(resp, 'candidates') and resp.candidates:
                parts = getattr(resp.candidates[0], 'content', None)
                if parts and getattr(parts, 'parts', None):
                    return ''.join(getattr(p, 'text', '') for p in parts.parts if hasattr(p, 'text'))
            return ''
        except Exception as e:
            raise RuntimeError(f'Gemini API error: {e}')
