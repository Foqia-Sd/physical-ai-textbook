// docusaurus/src/pages/login.js - Simple working version
import React, { useState } from 'react';
import Layout from '@theme/Layout';

function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    // Placeholder for login functionality
    console.log('Login attempt with:', { email, password });

    // Simulate login
    try {
      // In a real implementation, we would call the actual auth API
      // await signIn({ email, password });
      alert('Login functionality would connect to auth server');
    } catch (err) {
      setError('Login failed. Please try again.');
    }
  };

  return (
    <Layout title="Login" description="Sign in to your account">
      <div className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="padding-vert--md">
              <h1 className="text--center">Sign In</h1>

              <form onSubmit={handleSubmit} className="margin-vert--lg">
                <div className="form-group margin-bottom--md">
                  <label htmlFor="email">Email</label>
                  <input
                    type="email"
                    id="email"
                    className="form-control"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
                <div className="form-group margin-bottom--md">
                  <label htmlFor="password">Password</label>
                  <input
                    type="password"
                    id="password"
                    className="form-control"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                  />
                </div>
                {error && (
                  <div className="alert alert--danger margin-bottom--md">
                    {error}
                  </div>
                )}
                <button
                  type="submit"
                  className="button button--primary button--block"
                >
                  Sign In
                </button>
              </form>

              <div className="margin-vert--lg text--center">
                <p>
                  Don't have an account? <a href="/register">Sign up</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default LoginPage;