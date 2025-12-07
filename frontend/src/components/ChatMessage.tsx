import React from 'react';
import { ChatMessage as ChatMessageType } from '../services/chatService';

interface ChatMessageProps {
  message: ChatMessageType;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message }) => {
  const isUser = message.role === 'user';
  
  return (
    <div className={`chat-message ${isUser ? 'user-message' : 'assistant-message'}`}>
      <div className="message-bubble">
        <p>{message.content}</p>
        {message.sources && message.sources.length > 0 && (
          <div className="message-sources">
            <details>
              <summary>Sources</summary>
              <ul>
                {message.sources.map((source, index) => (
                  <li key={index}>
                    <strong>Source:</strong> {source.source}
                    <p>{source.content.substring(0, 150)}{source.content.length > 150 ? '...' : ''}</p>
                  </li>
                ))}
              </ul>
            </details>
          </div>
        )}
      </div>
      <div className="message-timestamp">
        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
    </div>
  );
};

export default ChatMessage;