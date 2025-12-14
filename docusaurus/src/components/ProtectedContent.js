// docusaurus/src/components/ProtectedContent.js
import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const ProtectedContent = ({ children, fallback = <div>Please sign in to view this content.</div> }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!user) {
    return fallback;
  }

  return children;
};

export default ProtectedContent;