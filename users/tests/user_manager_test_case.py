from django.test import TestCase
from users.models import UserModel


class UserManagerTestCase(TestCase):
    """Test cases for the custom UserManager"""

    def setUp(self):
        """Set up test data for users and superusers before each test"""
        self.user_data = {
            "email": "testuser@example.com",
            "username": "testuser",
            "phone_number": "+989123456789",
            "password": "SecurePass123!",
        }
        self.superuser_data = {
            "email": "admin@example.com",
            "username": "adminuser",
            "phone_number": "+989198765432",
            "password": "AdminPass123!",
        }

    def test_create_user_successfully(self):
        """Test creating a regular user with valid data"""
        user = UserModel.objects.create_user(**self.user_data)

        # Ensure user properties are correctly set
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.username, "testuser")
        self.assertTrue(
            user.check_password("SecurePass123!")
        )  # Ensure password is hashed correctly
        self.assertFalse(user.is_staff)  # Regular users shouldn't have admin access
        self.assertFalse(user.is_superuser)  # Regular users shouldn't be superusers

    def test_create_superuser_successfully(self):
        """Test creating a superuser with valid data"""
        superuser = UserModel.objects.create_superuser(**self.superuser_data)

        # Ensure superuser properties are correctly set
        self.assertEqual(superuser.email, "admin@example.com")
        self.assertEqual(superuser.username, "adminuser")
        self.assertTrue(superuser.check_password("AdminPass123!"))
        self.assertTrue(superuser.is_staff)  # Superusers must have admin access
        self.assertTrue(
            superuser.is_superuser
        )  # Superusers should have full permissions

    def test_create_user_without_email_fails(self):
        """Test that creating a user without an email raises an error"""
        with self.assertRaises(ValueError):
            UserModel.objects.create_user(
                email=None,
                username="userwithoutemail",
                phone_number="+989112345678",
                password="Pass123!",
            )

    def test_create_user_without_username_fails(self):
        """Test that creating a user without a username raises an error"""
        with self.assertRaises(ValueError):
            UserModel.objects.create_user(
                email="nousername@example.com",
                username=None,
                phone_number="+989112345678",
                password="Pass123!",
            )

    def test_create_user_without_password_fails(self):
        """Test that creating a user without a password raises an error"""
        with self.assertRaises(ValueError):
            UserModel.objects.create_user(
                email="nopassword@example.com",
                username="nopassword",
                phone_number="+989112345678",
                password=None,
            )

    def test_username_is_lowercase(self):
        """Test that usernames are always stored in lowercase"""
        user = UserModel.objects.create_user(
            email="capitalusername@example.com",
            username="TestUser123",
            phone_number="+989123456789",
            password="TestPass123!",
        )
        self.assertEqual(
            user.username, "testuser123"
        )  # Should be converted to lowercase

    def test_superuser_must_have_is_staff_and_is_superuser(self):
        """Ensure that superusers have 'is_staff' and 'is_superuser' set to True"""
        superuser = UserModel.objects.create_superuser(**self.superuser_data)
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
