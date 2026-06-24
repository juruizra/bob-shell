"""
Secure Authentication Module

This module provides secure authentication services with:
- Parameterized SQL queries to prevent SQL injection
- Bcrypt password hashing
- Input validation
- Separation of concerns (SOLID principles)
- Secure session management
- Rate limiting for failed login attempts
"""

import secrets
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

try:
    import bcrypt
except ImportError:
    # Fallback for environments without bcrypt
    import hashlib
    bcrypt = None

from ..database.db_manager import DatabaseManager


# Configure secure logging (no sensitive data)
logger = logging.getLogger(__name__)


class PasswordHasher(ABC):
    """Abstract interface for password hashing"""
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hash a password securely"""
        pass
    
    @abstractmethod
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify a password against its hash"""
        pass


class BcryptPasswordHasher(PasswordHasher):
    """Secure password hashing using bcrypt"""
    
    def __init__(self, rounds: int = 12):
        """
        Initialize bcrypt hasher.
        
        Args:
            rounds: Number of bcrypt rounds (default: 12)
        """
        if bcrypt is None:
            raise ImportError("bcrypt library is required for secure password hashing")
        self.rounds = rounds
    
    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.
        
        Args:
            password: Plain text password
            
        Returns:
            Bcrypt hash as string
        """
        salt = bcrypt.gensalt(rounds=self.rounds)
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        return password_hash.decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """
        Verify a password against its bcrypt hash.
        
        Args:
            password: Plain text password to verify
            password_hash: Stored bcrypt hash
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                password_hash.encode('utf-8')
            )
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False


class InputValidator:
    """Validates user input to prevent injection attacks"""
    
    # Constants for validation rules
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 50
    MIN_PASSWORD_LENGTH = 8
    MAX_PASSWORD_LENGTH = 128
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """
        Validate username format and length.
        
        Args:
            username: Username to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not username or not isinstance(username, str):
            return False
        
        if len(username) < InputValidator.MIN_USERNAME_LENGTH:
            return False
        
        if len(username) > InputValidator.MAX_USERNAME_LENGTH:
            return False
        
        # Only allow alphanumeric and underscore
        if not username.replace('_', '').isalnum():
            return False
        
        return True
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """
        Validate password format and length.
        
        Args:
            password: Password to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not password or not isinstance(password, str):
            return False
        
        if len(password) < InputValidator.MIN_PASSWORD_LENGTH:
            return False
        
        if len(password) > InputValidator.MAX_PASSWORD_LENGTH:
            return False
        
        return True
    
    @staticmethod
    def validate_token(token: str) -> bool:
        """
        Validate session token format.
        
        Args:
            token: Token to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not token or not isinstance(token, str):
            return False
        
        # Token should be hex string of specific length
        if len(token) != 64:  # 32 bytes = 64 hex chars
            return False
        
        try:
            int(token, 16)  # Verify it's valid hex
            return True
        except ValueError:
            return False


class RateLimiter:
    """Manages rate limiting for failed login attempts"""
    
    MAX_FAILED_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize rate limiter.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def record_failed_attempt(self, username: str) -> None:
        """
        Record a failed login attempt.
        
        Args:
            username: Username that failed login
        """
        query = """
            INSERT INTO login_attempts (username, failed_attempts, last_failed_attempt)
            VALUES (?, 1, ?)
            ON CONFLICT(username) DO UPDATE SET
                failed_attempts = failed_attempts + 1,
                last_failed_attempt = ?
        """
        now = datetime.utcnow()
        self.db.execute_query(query, (username, now, now))
        logger.warning(f"Failed login attempt recorded for user: {username}")
    
    def reset_failed_attempts(self, username: str) -> None:
        """
        Reset failed login attempts after successful login.
        
        Args:
            username: Username to reset
        """
        query = "DELETE FROM login_attempts WHERE username = ?"
        self.db.execute_query(query, (username,))
    
    def is_locked_out(self, username: str) -> bool:
        """
        Check if user is locked out due to too many failed attempts.
        
        Args:
            username: Username to check
            
        Returns:
            True if locked out, False otherwise
        """
        query = """
            SELECT failed_attempts, last_failed_attempt
            FROM login_attempts
            WHERE username = ?
        """
        results = self.db.execute_query(query, (username,))
        
        if not results:
            return False
        
        failed_attempts, last_failed_str = results[0]
        
        if failed_attempts < self.MAX_FAILED_ATTEMPTS:
            return False
        
        # Check if lockout period has expired
        last_failed = datetime.fromisoformat(last_failed_str)
        lockout_expires = last_failed + timedelta(minutes=self.LOCKOUT_DURATION_MINUTES)
        
        if datetime.utcnow() > lockout_expires:
            # Lockout expired, reset attempts
            self.reset_failed_attempts(username)
            return False
        
        return True


class SessionManager:
    """Manages user sessions securely"""
    
    SESSION_DURATION_HOURS = 24
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize session manager.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def create_session(self, user_id: int) -> str:
        """
        Create a new session for a user.
        
        Args:
            user_id: User ID to create session for
            
        Returns:
            Session token
        """
        # Generate cryptographically secure random token
        token = secrets.token_hex(32)
        
        now = datetime.utcnow()
        expires_at = now + timedelta(hours=self.SESSION_DURATION_HOURS)
        
        query = """
            INSERT INTO sessions (token, user_id, created_at, expires_at)
            VALUES (?, ?, ?, ?)
        """
        self.db.execute_query(query, (token, user_id, now, expires_at))
        
        logger.info(f"Session created for user_id: {user_id}")
        return token
    
    def validate_session(self, token: str) -> Optional[int]:
        """
        Validate a session token and return user_id if valid.
        
        Args:
            token: Session token to validate
            
        Returns:
            User ID if session is valid, None otherwise
        """
        if not InputValidator.validate_token(token):
            return None
        
        query = """
            SELECT user_id, expires_at
            FROM sessions
            WHERE token = ?
        """
        results = self.db.execute_query(query, (token,))
        
        if not results:
            return None
        
        user_id, expires_at_str = results[0]
        expires_at = datetime.fromisoformat(expires_at_str)
        
        if datetime.utcnow() > expires_at:
            # Session expired, delete it
            self.delete_session(token)
            return None
        
        return user_id
    
    def delete_session(self, token: str) -> None:
        """
        Delete a session (logout).
        
        Args:
            token: Session token to delete
        """
        if not InputValidator.validate_token(token):
            return
        
        query = "DELETE FROM sessions WHERE token = ?"
        self.db.execute_query(query, (token,))
        logger.info("Session deleted")
    
    def cleanup_expired_sessions(self) -> None:
        """Remove all expired sessions from database"""
        query = "DELETE FROM sessions WHERE expires_at < ?"
        self.db.execute_query(query, (datetime.utcnow(),))


class UserRepository:
    """Repository for user data access"""
    
    def __init__(self, db_manager: DatabaseManager):
        """
        Initialize user repository.
        
        Args:
            db_manager: Database manager instance
        """
        self.db = db_manager
    
    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Find a user by username using parameterized query.
        
        Args:
            username: Username to search for
            
        Returns:
            User dict if found, None otherwise
        """
        # SECURE: Using parameterized query to prevent SQL injection
        query = "SELECT id, username, password_hash FROM users WHERE username = ?"
        results = self.db.execute_query(query, (username,))
        
        if not results:
            return None
        
        user_id, username, password_hash = results[0]
        return {
            'id': user_id,
            'username': username,
            'password_hash': password_hash
        }
    
    def create_user(self, username: str, password_hash: str) -> int:
        """
        Create a new user with parameterized query.
        
        Args:
            username: Username for new user
            password_hash: Hashed password
            
        Returns:
            New user ID
        """
        # SECURE: Using parameterized query to prevent SQL injection
        query = """
            INSERT INTO users (username, password_hash)
            VALUES (?, ?)
        """
        self.db.execute_query(query, (username, password_hash))
        
        # Get the created user's ID
        user = self.find_by_username(username)
        return user['id'] if user else 0


class AuthenticationService:
    """
    Main authentication service following Single Responsibility Principle.
    
    Coordinates authentication operations using injected dependencies.
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        session_manager: SessionManager,
        rate_limiter: RateLimiter,
        input_validator: InputValidator
    ):
        """
        Initialize authentication service with dependencies.
        
        Args:
            user_repository: Repository for user data access
            password_hasher: Password hashing service
            session_manager: Session management service
            rate_limiter: Rate limiting service
            input_validator: Input validation service
        """
        self.user_repo = user_repository
        self.password_hasher = password_hasher
        self.session_manager = session_manager
        self.rate_limiter = rate_limiter
        self.validator = input_validator
    
    def login(self, username: str, password: str) -> Optional[str]:
        """
        Authenticate a user and create a session.
        
        Args:
            username: Username to authenticate
            password: Password to verify
            
        Returns:
            Session token if successful, None otherwise
        """
        # Validate input
        if not self.validator.validate_username(username):
            logger.warning("Invalid username format in login attempt")
            return None
        
        if not self.validator.validate_password(password):
            logger.warning("Invalid password format in login attempt")
            return None
        
        # Check rate limiting
        if self.rate_limiter.is_locked_out(username):
            logger.warning(f"Login attempt for locked out user: {username}")
            return None
        
        # Find user with parameterized query (SQL injection safe)
        user = self.user_repo.find_by_username(username)
        
        if not user:
            # Record failed attempt even if user doesn't exist (prevent user enumeration)
            self.rate_limiter.record_failed_attempt(username)
            logger.info("Login failed: user not found")
            return None
        
        # Verify password using secure hashing
        if not self.password_hasher.verify_password(password, user['password_hash']):
            self.rate_limiter.record_failed_attempt(username)
            logger.info(f"Login failed: invalid password for user: {username}")
            return None
        
        # Successful login
        self.rate_limiter.reset_failed_attempts(username)
        token = self.session_manager.create_session(user['id'])
        
        logger.info(f"Successful login for user: {username}")
        return token
    
    def logout(self, token: str) -> bool:
        """
        Logout a user by invalidating their session.
        
        Args:
            token: Session token to invalidate
            
        Returns:
            True if successful, False otherwise
        """
        if not self.validator.validate_token(token):
            return False
        
        self.session_manager.delete_session(token)
        return True
    
    def validate_session(self, token: str) -> Optional[int]:
        """
        Validate a session token.
        
        Args:
            token: Session token to validate
            
        Returns:
            User ID if valid, None otherwise
        """
        return self.session_manager.validate_session(token)
    
    def register_user(self, username: str, password: str) -> bool:
        """
        Register a new user.
        
        Args:
            username: Username for new user
            password: Password for new user
            
        Returns:
            True if successful, False otherwise
        """
        # Validate input
        if not self.validator.validate_username(username):
            logger.warning("Invalid username format in registration")
            return False
        
        if not self.validator.validate_password(password):
            logger.warning("Invalid password format in registration")
            return False
        
        # Check if user already exists
        existing_user = self.user_repo.find_by_username(username)
        if existing_user:
            logger.info(f"Registration failed: username already exists: {username}")
            return False
        
        # Hash password securely
        password_hash = self.password_hasher.hash_password(password)
        
        # Create user with parameterized query (SQL injection safe)
        user_id = self.user_repo.create_user(username, password_hash)
        
        if user_id > 0:
            logger.info(f"User registered successfully: {username}")
            return True
        
        return False


# Factory function for creating authentication service with all dependencies
def create_authentication_service(db_path: str = "banking_app.db") -> AuthenticationService:
    """
    Factory function to create AuthenticationService with all dependencies.
    
    Args:
        db_path: Path to database file
        
    Returns:
        Configured AuthenticationService instance
    """
    db_manager = DatabaseManager(db_path)
    user_repository = UserRepository(db_manager)
    password_hasher = BcryptPasswordHasher()
    session_manager = SessionManager(db_manager)
    rate_limiter = RateLimiter(db_manager)
    input_validator = InputValidator()
    
    return AuthenticationService(
        user_repository=user_repository,
        password_hasher=password_hasher,
        session_manager=session_manager,
        rate_limiter=rate_limiter,
        input_validator=input_validator
    )


# Made with Bob
