# Authentication Setup for Docusaurus AI Textbook

This document describes the complete authentication setup for the Physical AI & Humanoid Robotics textbook website.

## Architecture Overview

The authentication system consists of:

1. **Auth Server** (`auth-server/`) - A dedicated Node.js server using Better Auth
2. **Docusaurus Client** - Frontend integration using React hooks and context API
3. **Proxy Configuration** - Routes authentication requests from Docusaurus to Auth Server

## Setup Instructions

### 1. Backend Setup (Auth Server)

1. **Install Dependencies**:
   ```bash
   cd auth-server
   npm install
   ```

2. **Environment Variables**: Create `.env` in the `auth-server` directory:
   ```env
   BETTER_AUTH_SECRET=your-super-secret-key-change-this-in-production
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ```

3. **Run the Auth Server**:
   ```bash
   cd auth-server
   npm run start
   ```
   
   Or for development with auto-restart:
   ```bash
   npm run dev
   ```

### 2. Frontend Setup (Docusaurus)

The Docusaurus project is already configured for authentication:

1. **Proxy Configuration**: Authentication requests are automatically forwarded to the auth server at port 8001
2. **Authentication Context**: Uses React Context API for state management
3. **Components**: Ready-to-use auth-aware components

### 3. Available Authentication Features

- **Sign Up**: Email/password registration
- **Sign In**: Email/password login
- **Social Logins**: Google and GitHub (when properly configured)
- **Session Management**: Automatic session persistence
- **Protected Content**: Components that show content only to authenticated users

### 4. Using Authentication in Components

The authentication system provides easy-to-use hooks and components:

```javascript
// In any component, import and use the Auth context
import { useAuth } from '../contexts/AuthContext';

function MyComponent() {
  const { user, loading, signIn, signOut } = useAuth();

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {user ? (
        <div>
          <p>Welcome, {user.email || user.name}!</p>
          <button onClick={signOut}>Sign Out</button>
        </div>
      ) : (
        <button onClick={() => signIn({ email: 'user@example.com', password: 'password' })}>
          Sign In
        </button>
      )}
    </div>
  );
}
```

### 5. Protecting Content

Use the `ProtectedContent` component to restrict access:

```javascript
import ProtectedContent from '../components/ProtectedContent';

function MyPage() {
  return (
    <ProtectedContent
      fallback={<div>Please sign in to view this content</div>}
    >
      <div>This content is only visible to signed-in users</div>
    </ProtectedContent>
  );
}
```

## Integration Points

1. **Navigation Bar**: The AuthNavbar component is displayed in the header showing user status
2. **Chat Widget**: Automatically includes authentication headers when making requests
3. **Page Protection**: Use ProtectedContent for restricted areas

## API Endpoints

The auth server provides the following endpoints:

- `/api/auth/sign-in/email` - Sign in with email/password
- `/api/auth/sign-up/email` - Register new user
- `/api/auth/session` - Get current session
- `/api/auth/sign-out` - End session
- `/api/auth/social/[provider]` - Social login (Google, GitHub)

## Testing Authentication

1. Start the auth server: `cd auth-server && npm run start`
2. Start the docusaurus site: `cd docusaurus && npm run start`
3. Visit the site and use the sign-in buttons in the navigation bar
4. Check the browser's developer tools Network tab to see auth requests

## Troubleshooting

- If the site appears blank, check browser console for JavaScript errors
- Ensure the auth server is running on port 8001 (not 8000)
- Check that credentials: 'include' is set on auth-related fetch requests
- Verify CORS settings allow requests between frontend and auth server