// docusaurus/src/pages/protected.js
import React from 'react';
import Layout from '@theme/Layout';
import ProtectedContent from '../components/ProtectedContent';

function ProtectedPage() {
  return (
    <Layout title="Protected Content" description="This page requires authentication">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--8 col--offset-2">
            <h1>Protected Content</h1>
            <p>This content is only visible to authenticated users.</p>
            
            <ProtectedContent>
              <div className="alert alert--success margin-vert--md">
                <h3>Welcome, authenticated user!</h3>
                <p>You are viewing protected content because you are signed in.</p>
                <p>Your email: <code id="user-email"></code></p>
              </div>
              
              <div className="margin-vert--lg">
                <a href="/" className="button button--primary">
                  Go Home
                </a>
              </div>
            </ProtectedContent>
            
            <ProtectedContent 
              fallback={
                <div className="alert alert--info margin-vert--md">
                  <h3>Please sign in to view this content</h3>
                  <p>You need to be authenticated to see the protected information.</p>
                  <div className="margin-vert--lg">
                    <a href="/login" className="button button--primary">
                      Sign In
                    </a>
                  </div>
                </div>
              }
            >
              {/* This content is only shown to authenticated users */}
              <div className="card margin-vert--lg">
                <div className="card__header">
                  <h3>Exclusive Content</h3>
                </div>
                <div className="card__body">
                  <p>This is special content that only authenticated users can access.</p>
                  <p>You can add premium content, user dashboards, or any other restricted information here.</p>
                </div>
              </div>
            </ProtectedContent>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default ProtectedPage;