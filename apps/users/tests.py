from django.test import TestCase

from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import date
from .models import User, UserProfile

class UserModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            user_type="C",
            phone="1234567890"
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.user_type, "C")
        self.assertEqual(self.user.phone, "1234567890")

    def test_user_type_choices(self):
        self.user.user_type = "O"
        self.user.save()
        self.assertEqual(self.user.user_type, "O")

class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            birth_date=date(1990, 1, 1),
            address="123 Test Street"
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.birth_date, date(1990, 1, 1))
        self.assertEqual(self.profile.address, "123 Test Street")

    def test_str_representation(self):
        expected_str = f"Profil de {self.user.username}"
        self.assertEqual(str(self.profile), expected_str)
