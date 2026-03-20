import pytest
from unittest.mock import Mock, MagicMock, patch
from datetime import datetime, timedelta
import jwt

from src.user.services import UserService
from src.user.models import UserModel
from src.user.dtos import UserSchema, LoginSchema


class TestUserServicePasswordOperations:
    """Test password hashing and verification operations"""
    
    def test_should_hash_password_successfully(self):
        """Should hash a password successfully"""
        # Arrange
        service = UserService()
        plain_password = "mySecurePassword123"
        
        # Act
        hashed = service.get_password_hash(plain_password)
        
        # Assert
        assert hashed is not None
        assert hashed != plain_password
        assert len(hashed) > 0
    
    def test_should_verify_correct_password_against_hash(self):
        """Should verify correct password against hash"""
        # Arrange
        service = UserService()
        plain_password = "mySecurePassword123"
        hashed = service.get_password_hash(plain_password)
        
        # Act
        result = service.verify_password(plain_password, hashed)
        
        # Assert
        assert result is True
    
    def test_should_reject_incorrect_password_against_hash(self):
        """Should reject incorrect password against hash"""
        # Arrange
        service = UserService()
        plain_password = "mySecurePassword123"
        wrong_password = "wrongPassword456"
        hashed = service.get_password_hash(plain_password)
        
        # Act
        result = service.verify_password(wrong_password, hashed)
        
        # Assert
        assert result is False


class TestUserServiceCreateUser:
    """Test user creation operations"""
    
    def test_should_create_new_user_successfully(self):
        """Should create a new user successfully"""
        # Arrange
        service = UserService()
        mock_db = Mock()
        mock_query = Mock()
        mock_filter = Mock()
        
        # Setup mock chain for username check
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None  # No existing user
        
        user_data = UserSchema(
            name="John Doe",
            username="johndoe",
            password="password123",
            email="john@example.com"
        )
        
        # Act
        result = service.create_user(user_data, mock_db)
        
        # Assert
        assert result is not None
        assert mock_db.add.called
        assert mock_db.commit.called
        assert mock_db.refresh.called
        
        # Verify the user object passed to add
        added_user = mock_db.add.call_args[0][0]
        assert added_user.name == "John Doe"
        assert added_user.username == "johndoe"
        assert added_user.email == "john@example.com"
        assert added_user.hash_password != "password123"  # Should be hashed
    
    def test_should_raise_error_when_username_exists(self):
        """Should raise ValueError when username already exists"""
        # Arrange
        service = UserService()
        mock_db = Mock()
        mock_query = Mock()
        mock_filter = Mock()
        
        # Setup mock to return existing user
        existing_user = UserModel(
            id=1,
            name="Existing User",
            username="johndoe",
            hash_password="hashed",
            email="existing@example.com"
        )
        
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = existing_user
        
        user_data = UserSchema(
            name="John Doe",
            username="johndoe",
            password="password123",
            email="john@example.com"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Username already exists"):
            service.create_user(user_data, mock_db)
        
        # Verify no database operations were performed
        assert not mock_db.add.called
        assert not mock_db.commit.called
    
    def test_should_raise_error_when_email_exists(self):
        """Should raise ValueError when email already exists"""
        # Arrange
        service = UserService()
        mock_db = Mock()
        
        # Create a more sophisticated mock that handles multiple filter calls
        def query_side_effect(model):
            mock_query = Mock()
            filter_call_count = [0]
            
            def filter_side_effect(*args, **kwargs):
                mock_filter = Mock()
                filter_call_count[0] += 1
                
                # First call (username check) returns None
                # Second call (email check) returns existing user
                if filter_call_count[0] == 1:
                    mock_filter.first.return_value = None
                else:
                    existing_user = UserModel(
                        id=1,
                        name="Existing User",
                        username="different_user",
                        hash_password="hashed",
                        email="john@example.com"
                    )
                    mock_filter.first.return_value = existing_user
                
                return mock_filter
            
            mock_query.filter.side_effect = filter_side_effect
            return mock_query
        
        mock_db.query.side_effect = query_side_effect
        
        user_data = UserSchema(
            name="John Doe",
            username="johndoe",
            password="password123",
            email="john@example.com"
        )
        
        # Act & Assert
        with pytest.raises(ValueError, match="Email already exists"):
            service.create_user(user_data, mock_db)
        
        # Verify no database operations were performed
        assert not mock_db.add.called
        assert not mock_db.commit.called
    
    def test_should_hash_password_before_storing(self):
        """Should hash password before storing"""
        # Arrange
        service = UserService()
        mock_db = Mock()
        mock_query = Mock()
        mock_filter = Mock()
        
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        plain_password = "plainTextPassword123"
        user_data = UserSchema(
            name="John Doe",
            username="johndoe",
            password=plain_password,
            email="john@example.com"
        )
        
        # Act
        service.create_user(user_data, mock_db)
        
        # Assert
        added_user = mock_db.add.call_args[0][0]
        assert added_user.hash_password != plain_password
        # Verify it's actually a valid hash by checking if we can verify it
        assert service.verify_password(plain_password, added_user.hash_password)


class TestUserServiceAuthentication:
    """Test user authentication operations"""
    
    @patch('src.user.services.settings')
    @patch('src.user.services.datetime')
    def test_should_authenticate_user_with_correct_credentials(self, mock_datetime, mock_settings):
        """Should authenticate user with correct credentials"""
        # Arrange
        service = UserService()
        mock_db = Mock()
        mock_query = Mock()
        mock_filter = Mock()
        
        # Setup settings mock
        mock_settings.SECRET_KEY = "test_secret_key"
        mock_settings.ALGORITHM = "HS256"
        mock_settings.EXP_TIME = 30
        
        # Setup datetime mock
        fixed_now = datetime(2024, 1, 1, 12, 0, 0)
        mock_datetime.now.return_value = fixed_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        
        # Create a user with hashed password
        plain_password = "password123"
        hashed_password = service.get_password_hash(plain_password)
        
        existing_user = UserModel(
            id=1,
            name="John Doe",
            username="johndoe",
            hash_password=hashed_password,
            email="john@example.com"
        )
        
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = existing_user
        
        login_data = LoginSchema(
            username="johndoe",
            password=plain_password
        )
        
        # Act
        token = service.authenticate_user(login_data, mock_db)
        
        # Assert
        assert token is not None
        assert isinstance(token, str)
        
        # Decode and verify token
        decoded = jwt.decode(token, "test_secret_key", algorithms=["HS256"])
        assert decoded["_id"] == 1
        expected_exp = (fixed_now + timedelta(minutes=30)).timestamp()
        assert decoded["exp"] == expected_exp
    
    def test_should_raise_error_for_nonexistent_username(self):
        """Should raise PermissionError for non-existent username"""
        # Arrange
        service = UserService()
        mock_db = Mock()
        mock_query = Mock()
        mock_filter = Mock()
        
        # Setup mock to return no user
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = None
        
        login_data = LoginSchema(
            username="nonexistent",
            password="password123"
        )
        
        # Act & Assert
        with pytest.raises(PermissionError, match="You entered wrong username and password"):
            service.authenticate_user(login_data, mock_db)
    
    def test_should_raise_error_for_incorrect_password(self):
        """Should raise PermissionError for incorrect password"""
        # Arrange
        service = UserService()
        mock_db = Mock()
        mock_query = Mock()
        mock_filter = Mock()
        
        # Create a user with hashed password
        correct_password = "correctPassword123"
        hashed_password = service.get_password_hash(correct_password)
        
        existing_user = UserModel(
            id=1,
            name="John Doe",
            username="johndoe",
            hash_password=hashed_password,
            email="john@example.com"
        )
        
        mock_db.query.return_value = mock_query
        mock_query.filter.return_value = mock_filter
        mock_filter.first.return_value = existing_user
        
        login_data = LoginSchema(
            username="johndoe",
            password="wrongPassword456"
        )
        
        # Act & Assert
        with pytest.raises(PermissionError, match="You entered wrong username and password"):
            service.authenticate_user(login_data, mock_db)
