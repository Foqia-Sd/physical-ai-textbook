// auth-server/server.js
import express from 'express';
import { betterAuth } from 'better-auth';
import { toNodeHandler } from 'better-auth/node';
import { createProxyMiddleware } from 'http-proxy-middleware';
import { memoryAdapter } from 'better-auth/adapters/memory';

// Initialize Better Auth with memory adapter
const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || 'a-very-long-secret-key-change-this-in-production',
  database: memoryAdapter(),
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false,
  },
  socialProviders: {
    google: {
      clientId: process.env.GOOGLE_CLIENT_ID,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    },
    github: {
      clientId: process.env.GITHUB_CLIENT_ID,
      clientSecret: process.env.GITHUB_CLIENT_SECRET,
    },
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
  },
});

const app = express();

// Add CORS middleware for development
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
  if (req.method === 'OPTIONS') {
    res.sendStatus(200);
  } else {
    next();
  }
});

// Middleware to parse JSON
app.use(express.json());

// Mount Better Auth routes using the Node.js handler
app.use('/api/auth', toNodeHandler(auth));

// Proxy endpoint to your existing Python backend
app.use('/ask', createProxyMiddleware({
  target: 'http://localhost:8000', // Your Python backend
  changeOrigin: true,
  pathRewrite: {
    '^/ask': '/ask', // Adjust if needed
  },
}));

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'auth-server' });
});

const PORT = process.env.PORT || 8001;
app.listen(PORT, () => {
  console.log(`Auth server running on port ${PORT}`);
  console.log(`Auth endpoints available at http://localhost:${PORT}/api/auth`);
});