# ChatWidget Component

A React chat component for the AI Tutor that connects to the FastAPI backend.

## Usage

```jsx
import ChatWidget from '@site/src/components/ChatWidget';

// Basic usage
<ChatWidget />

// With custom API URL
<ChatWidget apiUrl="https://your-api-domain.com" />
```

## Props

- `apiUrl` (optional): The base URL for the API server. Defaults to 'http://localhost:8000'

## Features

- Real-time chat interface
- User and AI message differentiation
- Typing indicators
- Auto-scrolling to latest messages
- Error handling
- Responsive design