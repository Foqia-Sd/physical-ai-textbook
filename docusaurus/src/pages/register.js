// docusaurus/src/pages/register.js - Simple working version
import React, { useState } from 'react';
import Layout from '@theme/Layout';

function RegisterPage() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState('');

  const handleSignUp = async (e) => {
    e.preventDefault();
    setError('');

    // Placeholder for registration functionality
    console.log('Registration attempt with:', formData);

    try {
      // In a real implementation, we would call the actual auth API
      // await signUp(formData);
      alert('Registration functionality would connect to auth server');
    } catch (err) {
      setError('Registration failed. Please try again.');
    }
  };

  return (
    <Layout title="Register" description="Create a new account">
      <div className="container margin-vert--xl">
        <div className="row">
          <div className="col col--6 col--offset-3">
            <div className="padding-vert--md">
              <h1 className="text--center">Create Account</h1>

              {error && (
                <div className="alert alert--danger margin-vert--md">
                  {error}
                </div>
              )}

              <form onSubmit={handleSignUp} className="margin-vert--lg">
                <div className="form-group margin-vert--md">
                  <label htmlFor="name">Full Name</label>
                  <input
                    type="text"
                    id="name"
                    className="form-control"
                    value={formData.name}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group margin-vert--md">
                  <label htmlFor="email">Email Address</label>
                  <input
                    type="email"
                    id="email"
                    className="form-control"
                    value={formData.email}
                    onChange={(e) => setFormData({...formData, email: e.target.value})}
                    required
                  />
                </div>

                <div className="form-group margin-vert--md">
                  <label htmlFor="password">Password</label>
                  <input
                    type="password"
                    id="password"
                    className="form-control"
                    value={formData.password}
                    onChange={(e) => setFormData({...formData, password: e.target.value})}
                    required
                    minLength="6"
                  />
                </div>

                <div className="margin-vert--lg">
                  <button
                    type="submit"
                    className="button button--primary button--block"
                  >
                    Create Account
                  </button>
                </div>
              </form>

              <div className="margin-vert--lg text--center">
                <p>
                  Already have an account? <a href="/login">Sign in</a>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default RegisterPage;