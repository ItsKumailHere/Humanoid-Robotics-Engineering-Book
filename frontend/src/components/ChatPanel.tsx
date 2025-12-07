import React, { useState, useEffect, useRef } from 'react';
import { sendChatMessage, ChatMessage as ChatMessageType } from '../services/chatService';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

interface ChatPanelProps {
  isOpen: boolean;
  onClose: () => void;
}

const ChatPanel: React.FC<ChatPanelProps> = ({ isOpen, onClose }) => {
  const [messages, setMessages] = useState<ChatMessageType[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (message: string) => {
    if (!message.trim() || isLoading) return;

    // Add user message to chat
    const userMessage: ChatMessageType = {
      id: Date.now().toString(),
      content: message,
      role: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Call the backend API
      const response = await sendChatMessage({
        message: message,
        include_sources: true,
      });

      // Add assistant response to chat
      const assistantMessage: ChatMessageType = {
        id: (Date.now() + 1).toString(),
        content: response.response,
        role: 'assistant',
        timestamp: new Date(),
        sources: response.sources,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      // Add error message to chat
      const errorMessage: ChatMessageType = {
        id: (Date.now() + 1).toString(),
        content: "Sorry, I'm having trouble connecting to the AI assistant right now. Please try again later.",
        role: 'assistant',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Add a welcome message when the chat first opens
  useEffect(() => {
    if (isOpen && messages.length === 0) {
      const welcomeMessage: ChatMessageType = {
        id: 'welcome',
        content: "Hello! I'm your AI assistant for the Humanoid Robotics textbook. Feel free to ask me any questions about the content.",
        role: 'assistant',
        timestamp: new Date(),
      };
      setMessages([welcomeMessage]);
    }
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className="chat-panel-container">
      <div className="chat-panel-overlay" onClick={onClose} />
      <div className="chat-panel">
        <div className="chat-header">
          <h3>AI Assistant</h3>
          <button className="chat-close-button" onClick={onClose} aria-label="Close chat">
            ×
          </button>
        </div>
        
        <div className="chat-messages">
          {messages.map((msg) => (
            <ChatMessage
              key={msg.id}
              message={msg}
            />
          ))}
          {isLoading && (
            <div className="chat-loading-indicator">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        
        <div className="chat-input-area">
          <ChatInput 
            onSendMessage={handleSendMessage} 
            disabled={isLoading}
          />
        </div>
      </div>
    </div>
  );
};

export default ChatPanel;