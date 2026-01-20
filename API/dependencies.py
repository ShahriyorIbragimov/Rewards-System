from database import SessionLocal
from passlib.context import CryptContext
from fastapi import HTTPException, status
from users.models import Users, Role
import hmac
import hashlib
import os
from urllib.parse import parse_qs, unquote
from dotenv import load_dotenv

load_dotenv()

print(os.getenv("API"))

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def getDB():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def parse_init_data(init_data: str) -> dict:
    """Parse the init_data string into a dictionary."""
    parsed = {}
    for param in init_data.split('&'):
        if '=' in param:
            key, value = param.split('=', 1)
            key = unquote(key)
            value = unquote(value)
            
            # Handle nested objects like user.id -> user: {id: ...}
            if '.' in key:
                parts = key.split('.')
                obj_name = parts[0]
                field_name = '.'.join(parts[1:])
                
                if obj_name not in parsed:
                    parsed[obj_name] = {}
                
                # Handle nested fields
                if isinstance(parsed[obj_name], dict):
                    parsed[obj_name][field_name] = value
            else:
                parsed[key] = value
    
    # Parse the user object from flattened keys
    if any(k.startswith('user.') for k in parsed.keys()):
        user_obj = {}
        for key, value in list(parsed.items()):
            if key.startswith('user.'):
                field = key[5:]  # Remove 'user.' prefix
                # Try to convert to appropriate type
                if value.lower() == 'true':
                    user_obj[field] = True
                elif value.lower() == 'false':
                    user_obj[field] = False
                elif field == 'id':
                    user_obj[field] = int(value)
                else:
                    user_obj[field] = value
                del parsed[key]
        if user_obj:
            parsed['user'] = user_obj
    
    return parsed

def verify_telegram_auth(init_data: str) -> bool:
    """Verify the init_data signature from Telegram."""
    # Split the hash from the rest of the data
    params = init_data.split('&')
    hash_param = None
    data_params = []
    
    for param in params:
        if param.startswith('hash='):
            hash_param = param[5:]  # Remove 'hash=' prefix
        else:
            data_params.append(param)
    
    if not hash_param:
        print("DEBUG: No hash found in init_data")
        return False
    
    # Reconstruct the data check string
    # Sort params and join with newline
    data_check_string = '\n'.join(sorted(data_params))
    
    # Create secret key from bot token
    secret_key = hashlib.sha256(os.getenv("API").encode()).digest()
    
    # Calculate HMAC-SHA256
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    print(f"DEBUG: Received hash: {hash_param}")
    print(f"DEBUG: Calculated hash: {calculated_hash}")
    print(f"DEBUG: Data check string:\n{data_check_string}")
    print(f"DEBUG: Secret key (bot token): {os.getenv('API')}")
    
    return calculated_hash == hash_param

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password):
    return pwd_context.hash(password)

def isAdmin(user: Users):
    if user.role == Role.admin:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="You are not allowed to perform this action."
    )

def isActive(object):
    if object.is_active:
        return True
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="This object is not active."
    )

