import os
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import jwt
import bcrypt

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "boardroom_ai_secret_key_1234567890_super_secure")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120

# Prompts typical of prompt injection or jailbreak attempts
PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?previous instructions",
    r"you are now in developer mode",
    r"system prompt override",
    r"bypass safety settings",
    r"instead of your normal instructions",
    r"disregard any rules",
    r"you must now act as",
    r"ignore the CEO",
    r"execute system commands",
    r"reveal your system prompt",
    r"forget what you were told",
]

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hashed password."""
    try:
        return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and validate JWT access token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def check_prompt_injection(text: str) -> bool:
    """Check user prompt for potential prompt injection or jailbreak patterns."""
    if not text:
        return False
    
    text_lower = text.lower()
    for pattern in PROMPT_INJECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return True
            
    # Check for excessive instructions mimicry
    if text_lower.count("system:") > 2 or text_lower.count("instruction:") > 2:
        return True
        
    return False

def sanitize_input(text: str) -> str:
    """Sanitize user input to prevent basic HTML/script injection."""
    if not text:
        return ""
    # Strip HTML tags
    clean = re.sub(r'<[^>]*>', '', text)
    return clean.strip()

def verify_role(user_role: str, required_roles: List[str]) -> bool:
    """Verify if the user role meets requirements."""
    # admin has all rights
    if user_role == "admin":
        return True
    return user_role in required_roles
