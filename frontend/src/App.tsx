import React, { useState, useEffect } from 'react';
import AudioVisualizer from './components/AudioVisualizer';
import ChatDisplay from './components/ChatDisplay';
import './App.css';

interface Message {
  type: 'ai_response' | 'audio_start' | 'audio_end';
  text?: string;
  timestamp: number;
}

function App() {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [isAISpeaking, setIsAISpeaking] = useState(false);
  const [aiResponses, setAiResponses] = useState<string[]>([]);

  useEffect(() => {
    const websocket = new WebSocket('ws://localhost:8000/ws');
    
    websocket.onopen = () => {
      setIsConnected(true);
      setWs(websocket);
    };
    
    websocket.onmessage = (event) => {
      const message: Message = JSON.parse(event.data);
      
      switch (message.type) {
        case 'ai_response':
          if (message.text) {
            setAiResponses(prev => [...prev, message.text!]);
          }
          break;
        case 'audio_start':
          setIsAISpeaking(true);
          break;
        case 'audio_end':
          setIsAISpeaking(false);
          break;
      }
    };
    
    websocket.onclose = () => {
      setIsConnected(false);
      setWs(null);
    };
    
    return () => {
      websocket.close();
    };
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>AI Voice Visualizer</h1>
        <div className={`connection-status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '🟢 Connected' : '🔴 Disconnected'}
        </div>
      </header>
      
      <main className="App-main">
        <AudioVisualizer isActive={isAISpeaking} />
        <ChatDisplay responses={aiResponses} />
      </main>
    </div>
  );
}

export default App;
