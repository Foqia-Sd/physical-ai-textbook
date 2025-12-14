// docusaurus/src/contexts/AuthProvider.js
import React from 'react';

// Placeholder AuthProvider to avoid import errors
// Original implementation was causing issues due to better-auth@0.0.1 compatibility problems
const AuthContext = React.createContext();

export const useAuthContext = () => {
  return React.useContext(AuthContext);
};

export const AuthProvider = ({ children }) => {
  // Return children directly as a fallback
  return children;
};