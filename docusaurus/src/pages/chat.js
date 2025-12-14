// Example usage of ChatWidget in a Docusaurus page
import React from 'react';
import ChatWidget from '@site/src/components/ChatWidget';

const ChatPage = () => {
  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px' }}>
      <h1>AI Tutor for Physical AI & Humanoid Robotics</h1>
      <p>Ask any questions about the textbook, and our AI tutor will assist you!</p>
      
      {/* The ChatWidget component */}
      <ChatWidget apiUrl="http://localhost:8000" />
    </div>
  );
};

export default ChatPage;