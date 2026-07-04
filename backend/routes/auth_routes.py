from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from models.user import UserLogin, User
from services.auth_service import AuthService, DEFAULT_USERS
from typing import Optional

router = APIRouter()
security = HTTPBearer()


# In-memory user storage for demo (use database in production)
users_db = {}

# Initialize default users
for user in DEFAULT_USERS:
    hashed_password = AuthService.hash_password(user["password"])
    users_db[user["email"]] = {
        "email": user["email"],
        "name": user["name"],
        "hashed_password": hashed_password,
        "is_active": True
    }


@router.post("/login")
async def login(user_login: UserLogin):
    """Authenticate user and return JWT token"""
    
    # Check if user exists
    user = users_db.get(user_login.email)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password"
        )
    
    # Verify password
    if not AuthService.verify_password(user_login.password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )
    
    # Create access token
    access_token = AuthService.create_access_token(
        data={"sub": user["email"], "name": user["name"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user["email"],
            "name": user["name"]
        }
    }


@router.get("/me")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user from JWT token"""
    token = credentials.credentials
    payload = AuthService.verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    
    email = payload.get("sub")
    user = users_db.get(email)
    
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    return {
        "email": user["email"],
        "name": user["name"]
    }


@router.post("/register")
async def register(user_login: UserLogin):
    """Register a new user (for demo purposes)"""
    
    # Check if user already exists
    if user_login.email in users_db:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    
    # Hash password and store user
    hashed_password = AuthService.hash_password(user_login.password)
    users_db[user_login.email] = {
        "email": user_login.email,
        "name": user_login.email.split("@")[0],  # Use email prefix as name
        "hashed_password": hashed_password,
        "is_active": True
    }
    
    # Create access token
    access_token = AuthService.create_access_token(
        data={"sub": user_login.email, "name": users_db[user_login.email]["name"]}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "email": user_login.email,
            "name": users_db[user_login.email]["name"]
        }
    }