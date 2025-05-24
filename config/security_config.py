"""
Security configuration settings for BrainVenture.
"""

# Security settings
ENABLE_AUTHENTICATION = False  # Set to True when user authentication is implemented
ENABLE_CONTENT_SECURITY_POLICY = False  # Set to True to enable CSP

# Password security
PASSWORD_MIN_LENGTH = 8
PASSWORD_REQUIRE_UPPERCASE = True
PASSWORD_REQUIRE_LOWERCASE = True
PASSWORD_REQUIRE_DIGITS = True
PASSWORD_REQUIRE_SPECIAL_CHARS = True

# Session settings
SESSION_EXPIRY_MINUTES = 60  # 1 hour
SESSION_REFRESH_ON_ACTIVITY = True

# Content Security Policy settings
# See https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP
CSP_CONFIG = {
    "default-src": ["'self'"],
    "script-src": ["'self'"],
    "style-src": ["'self'"],
    "img-src": ["'self'", "data:"],
    "font-src": ["'self'"],
    "connect-src": ["'self'"],
    "frame-src": ["'self'"],
    "object-src": ["'none'"],
    "base-uri": ["'self'"],
    "form-action": ["'self'"],
    "frame-ancestors": ["'self'"]
}

# Rate limiting
RATE_LIMIT_ENABLED = False
MAX_REQUESTS_PER_MINUTE = 60

# Anti-sharing protection
ENABLE_ANTI_SHARING = False  # Set to True to enable measures against account sharing
MAX_DEVICES_PER_USER = 3
DETECT_LOCATION_CHANGES = False
