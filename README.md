# AI Copilot Backend

A FastAPI-based backend service that powers the AI Copilot chat application. This service integrates with Google's Gemini API to provide intelligent AI-powered responses to user messages.

## Project Overview

The AI Copilot Backend is a RESTful API service built with FastAPI that handles chat message processing and AI response generation. It provides a simple yet powerful interface for the frontend to communicate with Google's Gemini AI model, with built-in security features including CORS protection and API key management.

## Prerequisites

Before setting up the backend, ensure you have the following installed:

- **Python 3.8+** (Python 3.9 or higher recommended)
- **pip** (Python package manager)
- **Google Gemini API Key** - Obtain from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Environment Variables

The backend requires environment variables to be configured in a `.env` file located in the `ai_copilot_backend/` directory.

### Required Environment Variables

- **`GEMINI_API_KEY`** (Required): Your Google Gemini API key for AI model access
  - Obtain from: https://makersuite.google.com/app/apikey
  - Format: String value (e.g., `AIzaSyB...`)

### Optional Environment Variables

- **`FRONTEND_ORIGIN`** (Optional): Additional frontend origin URL for CORS
  - Default: `http://localhost:3000` and `http://127.0.0.1:3000` are always allowed
  - Example: `https://myapp.example.com`
  
- **`GEMINI_MODEL`** (Optional): Gemini model to use
  - Default: `gemini-1.5-flash`
  - Other options: `gemini-1.5-pro`, `gemini-pro`

### Sample .env File

Create a file named `.env` in the `ai_copilot_backend/` directory with the following content:

```env
# Required: Your Google Gemini API Key
GEMINI_API_KEY=your_actual_gemini_api_key_here

# Optional: Additional frontend origin for CORS
# FRONTEND_ORIGIN=https://your-frontend-domain.com

# Optional: Specify Gemini model (default: gemini-1.5-flash)
# GEMINI_MODEL=gemini-1.5-flash
```

**⚠️ Security Warning**: 
- **Never commit your `.env` file to version control**
- Add `.env` to your `.gitignore` file
- Keep your API keys secure and rotate them regularly
- Use different API keys for development and production

## Installation and Running

### Step 1: Navigate to Backend Directory

```bash
cd ai-chat-assistant-4361/ai_copilot_backend
```

### Step 2: Create and Activate Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Create .env File

Create a `.env` file in the `ai_copilot_backend/` directory (see sample above) and add your `GEMINI_API_KEY`.

### Step 5: Run the Backend Server

```bash
# Development mode with auto-reload
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3001

# Production mode
uvicorn src.api.main:app --host 0.0.0.0 --port 3001
```

The backend will start on **port 3001** by default.

### Preview Environment

**Note**: In the Kavia preview system, services are started automatically. The backend will be available at:
- Local: `http://localhost:3001`
- Preview URL: Provided by the Kavia platform

## API Endpoints

### Health Check

**Endpoint**: `GET /`

**Description**: Health check endpoint to verify the service is running.

**Response**:
```json
{
  "status": "ok"
}
```

**Status Codes**:
- `200`: Service is operational

---

### Chat Message

**Endpoint**: `POST /api/chat`

**Description**: Send a message to the AI and receive a response.

**Request Body**:
```json
{
  "message": "Your message to the AI"
}
```

**Request Schema**:
- `message` (string, required): User message to send to the AI (minimum length: 1)

**Response**:
```json
{
  "reply": "AI-generated response",
  "error": null
}
```

**Response Schema**:
- `reply` (string): The AI's response message
- `error` (string|null): Error message if something went wrong, otherwise null

**Status Codes**:
- `200`: Success - Message processed and AI response returned
- `400`: Bad Request - Missing API key or invalid configuration
- `422`: Validation Error - Invalid request format
- `500`: Internal Server Error - Unexpected error during processing

**Example Request** (using cURL):
```bash
curl -X POST http://localhost:3001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, AI!"}'
```

**Example Response**:
```json
{
  "reply": "Hello! How can I assist you today?",
  "error": null
}
```

**Error Response Example**:
```json
{
  "detail": "Missing GEMINI_API_KEY environment variable"
}
```

---

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: http://localhost:3001/docs
- **ReDoc**: http://localhost:3001/redoc
- **OpenAPI JSON**: http://localhost:3001/openapi.json (also available at `interfaces/openapi.json`)

## Frontend Usage

The frontend should connect to this backend using the base URL and call the `/api/chat` endpoint. See the frontend README for details on configuration.

**Frontend Configuration**:
```env
REACT_APP_BACKEND_URL=http://localhost:3001
```

## Troubleshooting

### Issue: "Missing GEMINI_API_KEY environment variable"

**Cause**: The `.env` file is missing or doesn't contain the `GEMINI_API_KEY` variable.

**Solution**:
1. Create a `.env` file in the `ai_copilot_backend/` directory
2. Add your Gemini API key: `GEMINI_API_KEY=your_key_here`
3. Restart the backend server

---

### Issue: CORS Errors from Frontend

**Symptoms**: Frontend shows errors like "Access to XMLHttpRequest has been blocked by CORS policy"

**Cause**: The frontend origin is not allowed by the backend CORS configuration.

**Solution**:
1. Ensure the backend is running on port 3001
2. If using a custom frontend URL, add it to `.env`:
   ```env
   FRONTEND_ORIGIN=https://your-custom-domain.com
   ```
3. Restart the backend server
4. Default allowed origins: `http://localhost:3000`, `http://127.0.0.1:3000`

---

### Issue: "google-generativeai package not available"

**Cause**: The required Google Generative AI package is not installed.

**Solution**:
```bash
pip install google-generativeai>=0.7.0
```

Or reinstall all dependencies:
```bash
pip install -r requirements.txt
```

---

### Issue: Port 3001 Already in Use

**Symptoms**: Error message "Address already in use" when starting the server.

**Solution**:
```bash
# Find the process using port 3001
# On Linux/Mac:
lsof -i :3001

# On Windows:
netstat -ano | findstr :3001

# Kill the process or use a different port
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 3002
```

If you change the port, update the frontend's `REACT_APP_BACKEND_URL` accordingly.

---

### Issue: Slow or Timeout Responses

**Cause**: Gemini API may take time to generate responses, or network issues.

**Solution**:
1. Check your internet connection
2. Verify your Gemini API key is valid and has quota
3. Try a different model (e.g., `gemini-1.5-flash` is faster than `gemini-1.5-pro`)
4. Increase timeout in frontend `chatService.js` if needed

---

### Issue: Empty Responses from AI

**Cause**: The Gemini API returned an empty or malformed response.

**Solution**:
1. Check if your API key has remaining quota
2. Try a different prompt or question
3. Review Gemini API status: https://status.cloud.google.com/
4. Check backend logs for detailed error messages

## Testing

### Run Unit Tests

```bash
# Install test dependencies (if not already installed)
pip install pytest

# Run tests
pytest

# Run tests with coverage
pytest --cov=src
```

### Manual API Testing

Use the interactive Swagger UI at http://localhost:3001/docs to test endpoints manually.

## Project Structure

```
ai_copilot_backend/
├── src/
│   └── api/
│       ├── __init__.py
│       ├── main.py                 # FastAPI application and endpoints
│       ├── generate_openapi.py     # OpenAPI spec generator
│       ├── models/
│       │   ├── __init__.py
│       │   └── chat_models.py      # Pydantic request/response models
│       └── services/
│           ├── __init__.py
│           └── gemini_service.py   # Gemini API integration
├── interfaces/
│   └── openapi.json                # Generated OpenAPI specification
├── requirements.txt                # Python dependencies
└── .env                            # Environment variables (create this)
```

## Future Enhancements

### Supabase Integration (Optional)

The application architecture supports future integration with Supabase for:

- **Chat History Persistence**: Store conversation history in Supabase PostgreSQL
- **User Authentication**: Implement user accounts and session management
- **Multi-user Support**: Enable multiple users with separate chat histories
- **Real-time Sync**: Use Supabase real-time features for collaborative chats

**Planned Environment Variables for Supabase**:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

**Implementation Notes**:
- Install Supabase Python client: `pip install supabase`
- Create tables for users, conversations, and messages
- Add authentication middleware to protect endpoints
- Implement database models for persistence

### Other Planned Features

- **Rate Limiting**: Protect API from abuse
- **Caching**: Cache frequent responses to reduce API calls
- **Streaming Responses**: Stream AI responses in real-time
- **Multi-model Support**: Support for multiple AI models (OpenAI, Anthropic, etc.)
- **Conversation Context**: Maintain conversation history across messages
- **File Upload**: Support for document analysis and image inputs

## Security Best Practices

1. **Environment Variables**: Never commit `.env` files to version control
2. **API Keys**: Rotate API keys regularly and use different keys per environment
3. **CORS**: Only allow trusted frontend origins
4. **Rate Limiting**: Implement rate limiting in production (future enhancement)
5. **Input Validation**: All inputs are validated using Pydantic models
6. **Error Handling**: Sensitive error details are not exposed to clients
7. **HTTPS**: Use HTTPS in production environments
8. **Monitoring**: Set up logging and monitoring for production deployments

## Dependencies

Key dependencies (see `requirements.txt` for complete list):

- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for running FastAPI
- **google-generativeai**: Google's Gemini API client
- **pydantic**: Data validation using Python type annotations
- **python-dotenv**: Load environment variables from `.env`
- **httpx**: HTTP client for making requests

## Support and Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Google Gemini API**: https://ai.google.dev/docs
- **Python Documentation**: https://docs.python.org/3/

## License

This project is part of the AI Copilot application suite.
