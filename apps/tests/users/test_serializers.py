from django.test import TestCase

from apps.users.models import (
    CustomUser,
    UserProfile,
)

from apps.users.serializers import (
    CustomUserSerializer,
    UserProfileSerializer,
    DetailUserProfileSerializer,
)


class CustomUserSerializerTest(TestCase):

    def valid_data(self):

        return {
            "username": "jean",
            "first_name": "Jean",
            "last_name": "Paul",
            "email": "jean@example.com",
            "password1": "password123",
            "password2": "password123",
            "role": CustomUser.UserType.STAFF,
        }


    def test_valid_data(self):

        serializer = CustomUserSerializer(
            data=self.valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )


    def test_username_is_required(self):

        data = self.valid_data()
        data.pop("username")

        serializer = CustomUserSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "username",
            serializer.errors
        )

    def test_password1_is_required(self):

        data = self.valid_data()
        data.pop("password1")

        serializer = CustomUserSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "password1",
            serializer.errors
        )

    def test_password2_is_required(self):

        data = self.valid_data()
        data.pop("password2")

        serializer = CustomUserSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "password2",
            serializer.errors
        )


    def test_passwords_must_match(self):

        data = self.valid_data()

        data["password2"] = "different-password"

        serializer = CustomUserSerializer(
            data=data
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "password",
            serializer.errors
        )

    def test_matching_passwords_are_valid(self):

        data = self.valid_data()

        serializer = CustomUserSerializer(
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )


    def test_serializer_creates_user(self):

        serializer = CustomUserSerializer(
            data=self.valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        user = serializer.save()

        self.assertIsInstance(
            user,
            CustomUser
        )

        self.assertEqual(
            user.username,
            "jean"
        )

    def test_serializer_hashes_password(self):

        serializer = CustomUserSerializer(
            data=self.valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        user = serializer.save()

        self.assertNotEqual(
            user.password,
            "password123"
        )

        self.assertTrue(
            user.check_password("password123")
        )


    def test_creating_user_creates_profile(self):

        serializer = CustomUserSerializer(
            data=self.valid_data()
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        user = serializer.save()

        self.assertTrue(
            UserProfile.objects.filter(
                user=user
            ).exists()
        )


    def test_id_is_read_only(self):

        serializer = CustomUserSerializer()

        self.assertTrue(
            serializer.fields["id"].read_only
        )

    def test_password1_is_write_only(self):

        serializer = CustomUserSerializer()

        self.assertTrue(
            serializer.fields["password1"].write_only
        )

    def test_password2_is_write_only(self):

        serializer = CustomUserSerializer()

        self.assertTrue(
            serializer.fields["password2"].write_only
        )


    def test_empty_data_is_invalid(self):

        serializer = CustomUserSerializer(
            data={}
        )

        self.assertFalse(
            serializer.is_valid()
        )

    def test_none_data_is_invalid(self):

        serializer = CustomUserSerializer(
            data={
                "username": None,
                "password1": None,
                "password2": None,
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )


    def test_duplicate_username_is_invalid(self):

        CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        serializer = CustomUserSerializer(
            data=self.valid_data()
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "username",
            serializer.errors
        )


    def test_update_user(self):

        user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        data = {
            "username": "jean",
            "first_name": "Nouveau prénom",
            "last_name": "Nouveau nom",
            "email": "new@example.com",
            "password1": "password123",
            "password2": "password123",
            "role": CustomUser.UserType.STAFF,
        }

        serializer = CustomUserSerializer(
            instance=user,
            data=data
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        updated_user = serializer.save()

        self.assertEqual(
            updated_user.first_name,
            "Nouveau prénom"
        )

        self.assertEqual(
            updated_user.email,
            "new@example.com"
        )
        
        
        
class UserProfileSerializerTest(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="jean",
            password="password123"
        )

        self.profile = self.user.user_profile


    def test_valid_phone(self):

        serializer = UserProfileSerializer(
            instance=self.profile,
            data={
                "phone": "0700000000"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )


    def test_phone_too_short_is_invalid(self):

        serializer = UserProfileSerializer(
            instance=self.profile,
            data={
                "phone": "123"
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )

   
    def test_phone_too_long_is_invalid(self):

        serializer = UserProfileSerializer(
            instance=self.profile,
            data={
                "phone": "1" * 21
            }
        )

        self.assertFalse(
            serializer.is_valid()
        )

        self.assertIn(
            "phone",
            serializer.errors
        )


    def test_phone_with_exactly_10_characters_is_valid(self):

        serializer = UserProfileSerializer(
            instance=self.profile,
            data={
                "phone": "1234567890"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )


    def test_phone_with_exactly_20_characters_is_valid(self):

        serializer = UserProfileSerializer(
            instance=self.profile,
            data={
                "phone": "1" * 20
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

  
    def test_user_is_read_only(self):

        serializer = UserProfileSerializer()

        self.assertTrue(
            serializer.fields["user"].read_only
        )


    def test_update_phone(self):

        serializer = UserProfileSerializer(
            instance=self.profile,
            data={
                "phone": "0700000000"
            }
        )

        self.assertTrue(
            serializer.is_valid(),
            serializer.errors
        )

        profile = serializer.save()

        self.assertEqual(
            profile.phone,
            "0700000000"
        )
        
        
class DetailUserProfileSerializerTest(TestCase):

    def setUp(self):

        self.user = CustomUser.objects.create_user(
            username="jean",
            password="password123",
            first_name="Jean",
            last_name="Paul"
        )

        self.profile = self.user.user_profile

    def test_serializer_contains_user(self):

        serializer = DetailUserProfileSerializer(
            instance=self.profile
        )

        data = serializer.data

        self.assertIn(
            "user",
            data
        )

    def test_serializer_contains_phone(self):

        serializer = DetailUserProfileSerializer(
            instance=self.profile
        )

        self.assertIn(
            "phone",
            serializer.data
        )

    def test_user_is_nested(self):

        serializer = DetailUserProfileSerializer(
            instance=self.profile
        )

        self.assertIsInstance(
            serializer.data["user"],
            dict
        )