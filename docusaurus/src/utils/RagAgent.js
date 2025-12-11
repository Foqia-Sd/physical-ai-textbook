/**
 * RAG Agent utility to connect frontend to backend
 */
class RagAgent {
  constructor() {
    // Check if we're in a Node.js environment or browser
    // In browser, process might not be defined
    let backendUrl;
    if (typeof process !== 'undefined' && process.env) {
      // Node.js environment
      backendUrl = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';
    } else {
      // Browser environment - use default
      backendUrl = 'http://localhost:8000';
    }
    this.backendUrl = backendUrl;
  }

  setBackendUrl(url) {
    this.backendUrl = url;
  }

  async query(message, context = {}) {
    try {
      const response = await fetch(`${this.backendUrl}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: message,
          context: context
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend error: ${response.status}`);
      }

      const data = await response.json();
      return {
        response: data.response,
        sources: data.sources,
        context: data.context
      };
    } catch (error) {
      console.error('Error querying RAG agent:', error);
      throw error;
    }
  }

  async retrieve(query, topK = 5) {
    try {
      const response = await fetch(`${this.backendUrl}/retrieve`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query,
          top_k: topK
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend retrieval error: ${response.status}`);
      }

      const data = await response.json();
      return data.results;
    } catch (error) {
      console.error('Error retrieving from RAG:', error);
      throw error;
    }
  }

  async chat(message) {
    try {
      const response = await fetch(`${this.backendUrl}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: message
        }),
      });

      if (!response.ok) {
        throw new Error(`Backend chat error: ${response.status}`);
      }

      const data = await response.json();
      return data.answer;
    } catch (error) {
      console.error('Error in chat:', error);
      throw error;
    }
  }

  async healthCheck() {
    try {
      const response = await fetch(`${this.backendUrl}/health`);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }

  getTools() {
    return ['query', 'retrieve', 'chat', 'healthCheck'];
  }
}

export default new RagAgent();