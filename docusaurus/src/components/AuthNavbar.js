// docusaurus/src/components/AuthNavbar.js
import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const AuthNavbar = () => {
  const { user, loading, signIn, signOut } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="auth-navbar">
      {user ? (
        <div className="user-info">
          <span>Welcome, {user.email || user.name || 'User'}!</span>
          <button onClick={() => signOut()}>Sign Out</button>
        </div>
      ) : (
        <div className="auth-buttons">
          <button onClick={() => {
            // Example login call - you'd want to show a form instead
            signIn({ email: 'user@example.com', password: 'password' })
              .catch(err => console.error('Login failed:', err));
          }}>
            Sign In
          </button>
        </div>
      )}
    </div>
  );
};

export default AuthNavbar;