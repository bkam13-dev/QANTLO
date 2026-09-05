from django.test import TestCase

from apps.users.models import (
    CustomUser,
    UserProfile,
)


class UserProfileSignalTest(TestCase):

   
    def test_profile_is_created_automatically(self):

        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        self.assertTrue(
            UserProfile.objects.filter(
                user=user
            ).exists()
        )


    def test_only_one_profile_is_created(self):

        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        self.assertEqual(
            UserProfile.objects.filter(
                user=user
            ).count(),
            1
        )


    def test_updating_user_does_not_create_second_profile(self):

        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        user.first_name = "Jean"
        user.save()

        self.assertEqual(
            UserProfile.objects.filter(
                user=user
            ).count(),
            1
        )


    def test_existing_profile_is_not_replaced(self):

        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        profile = user.user_profile

        profile.phone = "0700000000"
        profile.save()

        user.first_name = "Jean"
        user.save()

        profile.refresh_from_db()

        self.assertEqual(
            profile.phone,
            "0700000000"
        )