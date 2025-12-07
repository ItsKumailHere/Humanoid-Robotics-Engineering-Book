import React, { useState, useEffect } from 'react';
import OriginalLayout from '@theme-original/Layout';
import ChatPanel from '../components/ChatPanel';
import FloatingChatButton from '../components/FloatingChatButton';

// Define the type for Layout props
type LayoutProps = {
  children: React.ReactNode;
  title?: string;
  description?: string;
  image?: string;
  keywords?: string[];
  permalink?: string;
  id?: string;
};

const Layout: React.FC<LayoutProps> = (props) => {
  const [isChatOpen, setIsChatOpen] = useState(false);
  const [chatComponents, setChatComponents] = useState<{
    ChatPanel: React.ComponentType<any> | null;
    FloatingChatButton: React.ComponentType<any> | null;
  }>({ ChatPanel: null, FloatingChatButton: null });

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  // Dynamically import components to avoid SSR issues
  useEffect(() => {
    if (typeof window !== 'undefined') {
      Promise.all([
        import('../components/ChatPanel'),
        import('../components/FloatingChatButton')
      ]).then(([chatPanelModule, floatingButtonModule]) => {
        setChatComponents({
          ChatPanel: chatPanelModule.default,
          FloatingChatButton: floatingButtonModule.default
        });
      });
    }
  }, []);

  // Close chat when pressing Escape key
  useEffect(() => {
    const handleEscKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape' && isChatOpen) {
        setIsChatOpen(false);
      }
    };

    // Only add event listener if we're on the client side
    if (typeof window !== 'undefined') {
      window.addEventListener('keydown', handleEscKey);
    }

    return () => {
      if (typeof window !== 'undefined') {
        window.removeEventListener('keydown', handleEscKey);
      }
    };
  }, [isChatOpen]);

  return (
    <>
      <OriginalLayout {...props} />
      {chatComponents.FloatingChatButton && (
        <chatComponents.FloatingChatButton 
          onClick={toggleChat} 
          isOpen={isChatOpen} 
        />
      )}
      {chatComponents.ChatPanel && (
        <chatComponents.ChatPanel 
          isOpen={isChatOpen} 
          onClose={toggleChat} 
        />
      )}
    </>
  );
};

export default Layout;