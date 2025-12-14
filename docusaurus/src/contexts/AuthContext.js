// docusaurus/src/contexts/AuthContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';
import { getSession, signIn as signInClient, signOut as signOutClient, signUp as signUpClient } from '../utils/auth-client';

const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      try {
        setLoading(true); // Set loading to true when starting to check
        const session = await getSession();
        setUser(session?.user || null); // Only pass the user object, not the full session
      } catch (error) {
        console.error('Error checking session:', error);
        setUser(null);
      } finally {
        setLoading(false);
      }
    };

    checkSession();
  }, []);

  const value = {
    user,
    loading,
    signIn: async (credentials) => {
      try {
        const result = await signInClient(credentials);
        setUser(result.user);
        return result;
      } catch (error) {
        console.error('Sign in error in context:', error);
        throw error;
      }
    },
    signOut: async () => {
      try {
        const result = await signOutClient();
        setUser(null);
        return result;
      } catch (error) {
        console.error('Sign out error in context:', error);
        setUser(null);
        return { success: false };
      }
    },
    signUp: async (userData) => {
      try {
        const result = await signUpClient(userData);
        setUser(result.user);
        return result;
      } catch (error) {
        console.error('Sign up error in context:', error);
        throw error;
      }
    }
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};