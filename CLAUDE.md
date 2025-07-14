# Robot Head Project - Go Architecture Plan

## Project Goal
Build a physical robot head with LED mouth visualization that can:
- Have conversations using voice input/output
- Display LED patterns synchronized with speech
- Scale to multiple robot heads in the future
- Demonstrate professional Go system architecture

## Current State
- Python implementation working locally (app.py, audio/, llm/)
- Uses Vosk for speech-to-text, OpenAI API, gTTS for text-to-speech
- Needs conversion to scalable Go architecture

## Planned Architecture
```
robot-head/
├── server/     # Go server (AI processing, conversation management)
├── client/     # Go client (hardware: mic, speakers, LEDs)  
├── shared/     # Common types/protocols
└── docker-compose.yml
```

**Current Setup:** Both components run on same Pi, communicate via localhost
**Future Setup:** Server can move to cloud, clients connect remotely

## Todo List Status
- Design Go architecture with client/server separation
- Build Go server with WebSocket support for real-time communication
- Implement Go client for hardware interaction (mic, speakers, LEDs)
- Add audio processing, OpenAI integration, TTS in server
- Design LED mouth visualization patterns
- Add session management and configuration system

## Communication Protocol
- WebSocket for real-time audio/LED data streaming
- REST API for configuration and status
- Shared message types for clean interfaces

## Key Technical Decisions
- Go for performance and professional credibility
- WebSocket for real-time LED synchronization with audio
- Separated concerns for future scalability
- Docker support for easy deployment