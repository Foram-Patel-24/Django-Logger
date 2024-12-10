from django.test import TestCase
from user.models import User 

class UserCategoryTest(TestCase):

    def setUp(self):
        print("Test Case Called.")
        User.objects.create_user(username="admin", email="admin@example.com", password="password123", status="Active", is_active=True)
        User.objects.create_user(username="testuser", email="test@example.com", password="password123", status="Inactive", is_active=False)

    def test_show_all_users(self):
        users = User.objects.all()

        print("\nAll Users in Database:")
        for user in users:
            print({
                'id': user.id,
                'username': user.username,
                'email': user.email                
            })

        self.assertTrue(users.exists(), "No users found in the database")

        for user in users:
            self.assertIsNotNone(user.email, f"User with ID {user.id} has no email")
