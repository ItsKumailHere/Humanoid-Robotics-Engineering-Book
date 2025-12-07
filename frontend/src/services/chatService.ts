/**
 * API service for RAG chat functionality
 * Connects to the existing backend RAG endpoint
 */

// Base URL for API requests
// Using browser-compatible approach for Docusaurus
let API_BASE_URL = 'http://localhost:8000'; // default fallback

// Check for custom API URL in a browser-compatible way
if (typeof window !== 'undefined') {
  // Option 1: Check for custom config in window object
  if ((window as any).CHAT_API_BASE_URL) {
    API_BASE_URL = (window as any).CHAT_API_BASE_URL;
  }
  // Option 2: Check for environment variables in a browser context
  else if ((window as any).env && (window as any).env.REACT_APP_API_BASE_URL) {
    API_BASE_URL = (window as any).env.REACT_APP_API_BASE_URL;
  }
}

/**
 * Interface for chat messages
 */
export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
  sources?: Array<{
    content: string;
    source: string;
    metadata?: Record<string, any>;
  }>;
}

/**
 * Interface for chat request
 */
export interface ChatRequest {
  message: string;
  include_sources?: boolean;
}

/**
 * Interface for chat response
 */
export interface ChatResponse {
  response: string;
  sources?: Array<{
    content: string;
    source: string;
    metadata?: Record<string, any>;
  }>;
}

/**
 * Send a message to the RAG chatbot API
 * @param {ChatRequest} request - The chat request containing the message
 * @returns {Promise<ChatResponse>} The response from the chatbot
 */
export const sendChatMessage = async (request: ChatRequest): Promise<ChatResponse> => {
  try {
    const response = await fetch(`${API_BASE_URL}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        message: request.message,
        include_sources: request.include_sources || false,
      }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error sending chat message:', error);
    throw error;
  }
};

/**
 * Get health status of the RAG chatbot API
 * @returns {Promise<{status: string, rag_initialized: boolean}>} The health status
 */
export const getChatHealth = async (): Promise<{status: string, rag_initialized: boolean}> => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const result = await response.json();
    return result;
  } catch (error) {
    console.error('Error checking chat health:', error);
    throw error;
  }
};