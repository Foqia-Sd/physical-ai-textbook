# Better Auth Integration for Docusaurus - Dedicated Auth Server Approach

This document describes how to set up and use Better Auth authentication with your Docusaurus site using a dedicated authentication server.

## Setup Instructions

### 1. Backend Setup (Dedicated Auth Server)

1. **Install Dependencies** in the `auth-server` directory:
   ```bash
   cd auth-server
   npm install
   ```

2. **Environment Variables**: Add the following to your `auth-server/.env` file:
   ```env
   BETTER_AUTH_SECRET=your-super-secret-key-change-this-in-production
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ```

3. **Run the Auth Server**: The auth server runs separately on port 8001:
   ```bash
   cd auth-server
   npm run start
   ```

   Or for development:
   ```bash
   cd auth-server
   npm run dev
   ```

### 2. Frontend Setup (Docusaurus)

1. **Proxy Configuration**: The Docusaurus development server is configured to proxy `/api/auth` requests to the auth server running on port 8001 via `docusaurus.proxy.config.js`
2. **Run Docusaurus** (make sure auth server is running first):
   ```bash
   cd docusaurus
   npm run start
   ```

### 3. Authentication Flow

- Auth Server handles all authentication logic at `http://localhost:8001/api/auth/*`
- Docusaurus development server proxies requests from `/api/auth` to auth server
- Session cookies are shared between the two services during development
- In production, both would be served from the same domain

### 4. Using Authentication in Your Components

The React Context API provides authentication state throughout the application:

```javascript
import { useAuth } from '../contexts/AuthContext';

// Example usage:
function MyComponent() {
  const { user, loading, signIn, signOut } = useAuth();

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      {user ? (
        <div>
          Welcome, {user.email || user.name}!
          <button onClick={() => signOut()}>Sign Out</button>
        </div>
      ) : (
        <button onClick={() => signIn({ email: 'email@example.com', password: 'password' })}>
          Sign In
        </button>
      )}
    </div>
  );
}
```

### 5. Protecting Content

Use the `ProtectedContent` component to show content only to authenticated users:

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

## Configuration Notes

- Authentication routes are available at `/api/auth` via proxy to the auth server
- The frontend proxy configuration is in `docusaurus.proxy.config.js`
- Session cookies are handled automatically by the browser when credentials: 'include' is set
- Social login providers (Google, GitHub) can be enabled by setting the environment variables

## Security Considerations

1. **Development**:
   - The current setup uses a memory adapter, so sessions are lost when the server restarts
   - Credentials are sent with each request via credentials: 'include'

2. **Production**:
   - Change the `BETTER_AUTH_SECRET` to a strong, randomly generated key
   - Use HTTPS in production
   - Consider using a persistent database adapter instead of memory adapter
   - Set proper CORS policies limiting origins

3. **Environment Variables**:
   - Never commit secrets to version control
   - Use different secrets for development and production
   - The memory adapter is fine for development but use a proper database in production