import React from 'react';

interface ChatDisplayProps {
  responses: string[];
}

const ChatDisplay: React.FC<ChatDisplayProps> = ({ responses }) => {
  return (
    <div className="chat-display">
      <h3>AI Responses</h3>
      <div className="responses-container">
        {responses.length === 0 ? (
          <p className="no-responses">Waiting for AI to speak...</p>
        ) : (
          responses.map((response, index) => (
            <div key={index} className="response-item">
              <div className="response-bubble">
                {response}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default ChatDisplay;