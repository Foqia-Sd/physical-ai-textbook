import React, { useState, useRef, useEffect } from 'react';
import styles from './styles.module.css';

// We'll initialize ragAgent in the component
let ragAgent = null;

const initialMessages = [];

function Message({ sender, text }) {
  return (
    <div className={`${styles.message} ${sender === 'ai' ? styles.aiMessage : styles.userMessage}`}>
      <div className={styles.messageContent}>{text}</div>
    </div>
  );
}

export default function ChatWidget() {
  const [isOpen, setIsOpen] = useState(false); // Start closed to avoid potential initialization issues
  const [messages, setMessages] = useState(initialMessages);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState('');
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Effect to handle text selection
  useEffect(() => {
    if (typeof window !== 'undefined' && window.getSelection) {
      const handleMouseUp = () => {
        const selection = window.getSelection().toString().trim();
        if (selection) {
          setSelectedText(selection);
          if (!isOpen) {
            setIsOpen(true); // Open chat if text is selected
          }
        }
      };

      document.addEventListener('mouseup', handleMouseUp);
      return () => document.removeEventListener('mouseup', handleMouseUp);
    }
  }, [isOpen]);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const toggleChat = () => setIsOpen(!isOpen);

  const handleInputChange = (e) => setInputValue(e.target.value);

  // Initialize RAG Agent
  const initializeRagAgent = () => {
    try {
      // Try using relative import path
      const ragAgentModule = require('../../utils/RagAgent');
      ragAgent = ragAgentModule.default;

      if (ragAgent && typeof ragAgent.setBackendUrl === 'function') {
        ragAgent.setBackendUrl('http://localhost:8000');
        console.log('RAG Agent initialized with backend connection');
        if (ragAgent.getTools) {
          console.log('Available tools:', ragAgent.getTools());
        }
      } else {
        console.error('RAG Agent is not properly loaded');
        // Create a mock ragAgent for graceful degradation
        ragAgent = {
          query: async (message, context = {}) => {
            console.error('RagAgent not available, returning mock response');
            return {
              response: "AI assistant is currently unavailable. Please try again later.",
              sources: [],
              context: context
            };
          },
          setBackendUrl: () => {},
          getTools: () => ['mock-tools']
        };
      }
    } catch (error) {
      console.error('Error initializing RAG Agent:', error);
      // Create a mock ragAgent for graceful degradation
      ragAgent = {
        query: async (message, context = {}) => {
          console.error('RagAgent not available due to error, returning mock response');
          return {
            response: "AI assistant is currently unavailable. Please try again later.",
            sources: [],
            context: context
          };
        },
        setBackendUrl: () => {},
        getTools: () => ['mock-tools']
      };
    }
  };

  // Call initialization when component mounts
  useEffect(() => {
    initializeRagAgent();
  }, []);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userMessage = { sender: 'user', text: inputValue };
    const newMessages = [...messages, userMessage];
    setMessages(newMessages);
    setInputValue('');
    setIsLoading(true);

    const context = selectedText;
    setSelectedText('');

    try {
      // Check if ragAgent is properly loaded before using it
      if (!ragAgent) {
        console.error('RagAgent is not loaded');
        setIsLoading(false);
        const errorMessage = { sender: 'ai', text: 'RagAgent is not loaded. Please refresh the page.' };
        setMessages((prev) => [...prev, errorMessage]);
        return;
      }

      // Use the RAG Agent to process the query
      const agentResponse = await ragAgent.query(userMessage.text, {
        selectedText: context // Pass the selected text as context
      });

      setIsLoading(false);

      // Format the agent response for display
      let responseText = agentResponse.response || 'No response generated.';

      if (agentResponse.sources && agentResponse.sources.length > 0) {
        const sourceUrls = [...new Set(agentResponse.sources.map(source => source.url))].slice(0, 3);
        if (sourceUrls.length > 0) {
          responseText += `\n\nSources: ${sourceUrls.join(', ')}`;
        }
      }

      const aiResponse = { sender: 'ai', text: responseText };
      setMessages((prev) => [...prev, aiResponse]);

    } catch (error) {
      console.error("RAG Agent error:", error);
      setIsLoading(false);
      const errorMessage = { sender: 'ai', text: 'Sorry, I encountered an error processing your request. Please try again.' };
      setMessages((prev) => [...prev, errorMessage]);
    }
  };

  const clearSelectedText = () => setSelectedText('');

  if (!isOpen) {
    return (
      <button className={styles.openChatButton} onClick={toggleChat}>
        <span>Chat</span>
      </button>
    );
  }

  return (
    <div className={styles.chatWindow}>
      <div className={styles.chatHeader}>
        <h2>AI Tutor</h2>
        <button onClick={toggleChat} className={styles.closeButton}>&times;</button>
      </div>
      <div className={styles.messagesContainer}>
        {messages.map((msg, index) => (
          <Message key={index} {...msg} />
        ))}
        {isLoading && <Message sender="ai" text="Thinking..." />}
        <div ref={messagesEndRef} />
      </div>
      <div className={styles.inputWrapper}>
        {selectedText && (
          <div className={styles.selectedTextIndicator}>
            <span>Context: "{selectedText.substring(0, 50)}..."</span>
            <button onClick={clearSelectedText}>&times;</button>
          </div>
        )}
        <form onSubmit={handleSendMessage} className={styles.inputArea}>
          <input
            type="text"
            value={inputValue}
            onChange={handleInputChange}
            placeholder="Ask a question..."
            className={styles.inputField}
            disabled={isLoading}
          />
          <button type="submit" className={styles.sendButton} disabled={isLoading}>
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
