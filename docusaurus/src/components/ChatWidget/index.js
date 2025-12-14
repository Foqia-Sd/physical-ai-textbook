import React, { useState, useEffect, useRef } from 'react';
import './styles.css';
import { addAuthHeaders } from '@site/src/utils/auth-client';

const Message = ({ sender, text, time }) => {
  const isUser = sender === 'user';
  return (
    <div className={`message ${isUser ? 'user-message' : 'ai-message'}`}>
      <div className="message-content">
        <span className="message-text">{text}</span>
        <span className="message-time">{time}</span>
      </div>
    </div>
  );
};

const ChatWidget = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    if (isOpen) {
      scrollToBottom();
    }
  }, [messages, isTyping, isOpen]);

  const handleSend = async () => {
    if (input.trim() === '') return;

    const currentInput = input;

    const userMessage = {
      sender: 'user',
      text: currentInput,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInput('');
    setIsTyping(true);

    try {
      // Use the proxy path which will be handled by Docusaurus dev server
      const response = await fetch('/ask', {
        method: 'POST',
        headers: addAuthHeaders({
          'Content-Type': 'application/json',
        }),
        body: JSON.stringify({ query: currentInput }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // FIX: backend returns data.answer, not data.response
      const aiMessage = {
        sender: 'ai',
        text: data.answer,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prevMessages => [...prevMessages, aiMessage]);

    } catch (error) {
      console.error('Error fetching AI response:', error);
      console.log('Backend might not be running. Showing mock response.');

      // Provide a mock response when backend is not available
      const mockResponse = "I'm the AI assistant. It seems the backend server is not running. Please ensure the backend is started on port 8000.";

      const errorMessage = {
        sender: 'ai',
        text: mockResponse,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };

      setMessages(prevMessages => [...prevMessages, errorMessage]);

    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div className="chat-floating-container">

      {isOpen && (
        <div className="chat-widget">

          <div className="chat-header">
            <h3>AI Assistant</h3>
          </div>

          <div className="chat-messages">
            {messages.length === 0 && !isTyping ? (
              <div className="welcome-message">
                <p>Welcome! Ask me anything about the content of this textbook.</p>
              </div>
            ) : (
              messages.map((msg, index) => (
                <Message
                  key={index}
                  sender={msg.sender}
                  text={msg.text}
                  time={msg.time}
                />
              ))
            )}

            {isTyping && (
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>

          <div className="chat-input-form">
            <input
              type="text"
              className="chat-input"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
              disabled={isTyping}
            />

            <button
              className="send-button"
              onClick={handleSend}
              disabled={isTyping || input.trim() === ''}
            >
              Send
            </button>
          </div>

        </div>
      )}

      {/* Floating bubble button */}
      <button className="chat-floating-button" onClick={toggleChat}>
        {isOpen ? '✕' : '💬'}
      </button>

    </div>
  );
};

export default ChatWidget;