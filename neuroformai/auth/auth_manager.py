import bcrypt
from database.queries import create_user, get_user_by_username


class AuthManager:
    """Handles user registration and authentication with bcrypt password hashing."""

    @staticmethod
    def hash_password(password):
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(password, password_hash):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )

    @staticmethod
    def signup(username, password, full_name):
        """
        Register a new user.
        Returns (success: bool, message: str, user_id: str or None).
        """
        if not username or not password:
            return False, "Username and password are required.", None

        if len(username) < 3:
            return False, "Username must be at least 3 characters.", None

        if len(password) < 6:
            return False, "Password must be at least 6 characters.", None

        existing = get_user_by_username(username)
        if existing:
            return False, "Username already taken.", None

        password_hash = AuthManager.hash_password(password)
        user_id = create_user(username, password_hash, full_name or username)
        return True, "Account created successfully!", user_id

    @staticmethod
    def login(username, password):
        """
        Authenticate a user.
        Returns (success: bool, message: str, user_data: dict or None).
        """
        if not username or not password:
            return False, "Username and password are required.", None

        user = get_user_by_username(username)
        if not user:
            return False, "User not found.", None

        if not AuthManager.verify_password(password, user["password_hash"]):
            return False, "Incorrect password.", None

        user_data = {
            "user_id": str(user["_id"]),
            "username": user["username"],
            "full_name": user.get("full_name", user["username"]),
        }
        return True, f"Welcome back, {user_data['full_name']}!", user_data
