from django.core.exceptions import ValidationError
from django.test import TestCase

from apps.users.models import CustomUser, UserProfile


class CustomUserModelTest(TestCase):


    def test_create_user(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        self.assertIsNotNone(user.id)
        self.assertEqual(user.username, "jean")

   

    def test_user_id_is_uuid(self):
        import uuid

        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        self.assertIsInstance(user.id, uuid.UUID)

    def test_user_id_is_unique(self):
        user1 = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        user2 = CustomUser.objects.create_user(
            username="paul",
            password="password123"
        )

        self.assertNotEqual(
            user1.id,
            user2.id
        )

    
    def test_default_role_is_staff(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        self.assertEqual(
            user.role,
            CustomUser.UserType.STAFF
        )

    def test_admin_role(self):
        user = CustomUser.objects.create_user(
            username="admin",
            password="password123",
            role=CustomUser.UserType.ADMIN
        )

        self.assertEqual(
            user.role,
            CustomUser.UserType.ADMIN
        )

    def test_manager_role(self):
        user = CustomUser.objects.create_user(
            username="manager",
            password="password123",
            role=CustomUser.UserType.MANAGER
        )

        self.assertEqual(
            user.role,
            CustomUser.UserType.MANAGER
        )

    def test_staff_role(self):
        user = CustomUser.objects.create_user(
            username="staff",
            password="password123",
            role=CustomUser.UserType.STAFF
        )

        self.assertEqual(
            user.role,
            CustomUser.UserType.STAFF
        )

   
    def test_username_is_required(self):
        user = CustomUser(
            password="password123"
        )

        with self.assertRaises(ValidationError):
            user.full_clean()


    def test_password_is_hashed(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        self.assertNotEqual(
            user.password,
            "password123"
        )

    def test_password_is_valid(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        self.assertTrue(
            user.check_password("password123")
        )

    def test_wrong_password_is_invalid(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        self.assertFalse(
            user.check_password("wrong-password")
        )


class UserProfileModelTest(TestCase):

    def test_create_profile(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        profile = UserProfile.objects.create(
            user=user,
            phone="0700000000"
        )

        self.assertIsNotNone(profile)
        self.assertEqual(profile.user, user)

   
    def test_user_can_access_profile(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        profile = user.user_profile

        self.assertEqual(
            profile.user,
            user
        )

    def test_profile_user_is_required(self):
        profile = UserProfile()

        with self.assertRaises(ValidationError):
            profile.full_clean()


    def test_phone_is_optional(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        profile = UserProfile.objects.create(
            user=user
        )

        self.assertIsNone(
            profile.phone
        )

  
    def test_user_can_have_only_one_profile(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        UserProfile.objects.create(
            user=user,
            phone="0700000000"
        )

        from django.db import IntegrityError

        with self.assertRaises(IntegrityError):
            UserProfile.objects.create(
                user=user,
                phone="0500000000"
            )

 
    def test_profile_is_deleted_when_user_is_deleted(self):
        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        profile = user.user_profile

        user.delete()

        self.assertFalse(
            UserProfile.objects.filter(
                id=profile.id
            ).exists()
        )