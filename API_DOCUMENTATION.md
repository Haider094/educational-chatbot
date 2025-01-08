# EduBot API Documentation

## Overview
EduBot is an educational chatbot that provides responses to educational queries using WebSocket communication and REST endpoints for token management.

## Base URL
```
https://your-domain:8080
```

## Authentication
All connections require an API token passed as a URL parameter.

### Token Format
```
?token=your_api_token
```

## Token Management Endpoints

### 1. Generate Token
**URL:** `POST /api/token/generate`

**Request Body:**
```json
{
    "user_id": "user123"
}
```

**Success Response:**
```json
{
    "status": 200,
    "token": "generated_api_token"
}
```

**Error Responses:**
```json
{
    "status": 400,
    "message": "User ID is required",
    "type": "ValidationError"
}
```

### 2. Refresh Token
**URL:** `POST /api/token/refresh`

**Request Body:**
```json
{
    "token": "expired_api_token"
}
```

**Success Response:**
```json
{
    "status": 200,
    "token": "new_api_token"
}
```

**Error Responses:**
```json
{
    "status": 400,
    "message": "Token is required",
    "type": "ValidationError"
}
```
```json
{
    "status": 401,
    "message": "Invalid or expired token",
    "type": "AuthenticationError"
}
```

## WebSocket Events

### 1. Connection
**URL Format:** 
```
https://your-domain:8080?token={API_TOKEN}&user_id={USER_ID}
```

**Required Parameters:**
- `token`: Your API authentication token
- `user_id`: Unique identifier for the user

**Success Response:**
```json
{
    "status": 200,
    "message": "Connected to EduBot!",
    "user_id": "user123"
}
```

**Error Responses:**
```json
{
    "status": 401,
    "message": "Authentication token is missing/invalid",
    "type": "AuthenticationError"
}
```
```json
{
    "status": 400,
    "message": "User ID is required",
    "type": "ValidationError"
}
```

### 2. Message Event
**Event Name:** `message`

**Request Format:**
```json
{
    "user_id": "user123",
    "message": "What is photosynthesis?"
}
```

**Success Response:**
```json
{
    "status": 200,
    "user_id": "user123",
    "data": "response_text",
    "message_type": "chat_response"
}
```

**Error Responses:**
```json
{
    "status": 400,
    "message": "Invalid JSON format",
    "type": "ValidationError"
}
```
```json
{
    "status": 403,
    "message": "User ID mismatch",
    "type": "AuthorizationError",
    "expected_user_id": "original_user_id"
}
```

### 3. Disconnect Event
**Event Name:** `disconnect`

**Response:**
```json
{
    "status": 200,
    "message": "Successfully disconnected from EduBot",
    "user_id": "user123"
}
```

## Predefined Queries
The following queries have preset responses:

| Query | Response |
|-------|----------|
| "who are you?" | "I am EduBot, your educational assistant." |
| "what are you?" | "I am an AI-powered educational assistant here to help with your learning needs." |
| "what can you do?" | "I can answer educational questions on a wide range of topics." |
| "what is your name?" | "My name is EduBot." |


## Error Types
- `AuthenticationError`: Token-related issues
- `ValidationError`: Invalid input data
- `AuthorizationError`: User ID mismatch
- `ServerError`: Internal server errors

## Best Practices
1. Always maintain the same user_id throughout a session
2. Handle connection errors gracefully
3. Implement reconnection logic
4. Keep messages in proper JSON format
5. Include both user_id and message in every request

## Rate Limiting
Currently, no explicit rate limiting is implemented. Please use the API responsibly.

## Notes
- All messages must be educational in nature
- Non-educational queries will be rejected
- Connection timeout: 60 seconds
- Ping interval: 25 seconds
