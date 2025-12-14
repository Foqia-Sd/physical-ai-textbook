import React from 'react';
import { AuthProvider } from '../contexts/AuthContext';

// Provide authentication context to the app
export default function Root({ children }) {
  return (
    <AuthProvider>
      {children}
    </AuthProvider>
  );
}