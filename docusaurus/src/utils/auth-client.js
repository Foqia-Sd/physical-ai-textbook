// docusaurus/src/utils/auth-client.js
// Custom authentication client for our backend auth system
// Updated to work with Better Auth server

import React from 'react';

let currentSession = null;
let isLoading = false;

// Function to get token from local storage
const getToken = () => {
  if (typeof window !== 'undefined') {
    return localStorage.getItem('session_token');
  }
  return null;
};

// Sign in function
const signIn = async (credentials = {}) => {
  try {
    const response = await fetch('/api/auth/sign-in/email', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: credentials.email,
        password: credentials.password
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Sign in failed');
    }

    const data = await response.json();
    if (typeof window !== 'undefined' && data.session_token) {
      localStorage.setItem('session_token', data.session_token);
      localStorage.setItem('user_email', data.user.email);
    }
    currentSession = data.user;
    return data;
  } catch (error) {
    console.error('Sign in error:', error);
    throw error;
  }
};

// Sign up function
const signUp = async (userData) => {
  try {
    const response = await fetch('/api/auth/sign-up/email', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: userData.email,
        password: userData.password,
        username: userData.username || userData.name // Better Auth expects username field
      }),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Sign up failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Sign up error:', error);
    throw error;
  }
};

// Sign out function
const signOut = async () => {
  try {
    // Clear local storage
    if (typeof window !== 'undefined') {
      localStorage.removeItem('session_token');
      localStorage.removeItem('user_email');
    }
    currentSession = null;

    // Call backend logout endpoint
    const response = await fetch('/api/auth/sign-out', {
      method: 'POST',
    });

    if (!response.ok) {
      console.warn('Logout request failed:', response.statusText);
    }

    return { success: response.ok };
  } catch (error) {
    console.error('Sign out error:', error);
    return { success: false };
  }
};

// Function to get session from storage or API
const getSession = async () => {
  try {
    const token = getToken();
    if (!token) return null;

    const response = await fetch('/api/auth/session', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });

    if (response.ok) {
      const sessionData = await response.json();
      if (sessionData && sessionData.user) {
        currentSession = sessionData.user;
        return sessionData;
      }
    }

    return null;
  } catch (error) {
    console.error('Error getting session:', error);
    return null;
  }
};

// Custom hook to manage session state
const useSession = () => {
  const [session, setSession] = React.useState(null);
  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    const fetchSession = async () => {
      setIsLoading(true);
      try {
        const sessionData = await getSession();
        setSession(sessionData);
      } catch (error) {
        console.error('Error fetching session:', error);
        setSession(null);
      } finally {
        setIsLoading(false);
      }
    };

    fetchSession();
  }, []);

  return { data: session, isLoading };
};

// For now, export functions directly since React hooks can't be used in regular functions
export { signIn, signUp, signOut, useSession, getSession, getToken };

// Simple useAuth function
export const useAuth = () => {
  return { signIn, signOut };
};

// Simple helper to check if user is authenticated
export const isAuthenticated = async () => {
  const session = await getSession();
  return !!session?.user;
};

// Helper to add auth headers to requests
export const addAuthHeaders = (headers = {}) => {
  const token = getToken();
  if (token) {
    return {
      ...headers,
      'Authorization': `Bearer ${token}`
    };
  }
  return headers;
};