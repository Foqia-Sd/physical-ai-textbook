# Simple authentication configuration
import os

# Configuration for the authentication system
AUTH_CONFIG = {
    "secret": os.getenv("BETTER_AUTH_SECRET", "a-very-long-secret-key-change-this-in-production"),
    "session_expiry": 7 * 24 * 60 * 60,  # 7 days in seconds
    "token_length": 32,
    "database_url": os.getenv("DATABASE_URL", "sqlite:///./better_auth.db"),
}