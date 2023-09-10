from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from profiles.models import Profile
from profiles.serializers import ProfileSerializer

PROFILES_LIST_URL = reverse("profile:profile-list")
PROFILE_OWN_URL = reverse("profile:my-profile")


def create_sample_user(**params):
    default = {
        "email": "test_user@test.com",
        "first_name": "Test",
        "last_name": "User",
    }
    default.update(params)
    return get_user_model().objects.create_user(
        **default, password="qwer1234"
    )


def get_profile(**params):
    user = create_sample_user(**params)
    return Profile.objects.get(user=user)


class AuthenticatedProfileTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_sample_user()
        self.client.force_authenticate(self.user)

    def test_list_profiles(self):
        get_profile(email="user2@mail.com")
        get_profile(email="user3@mail.com")
        profiles = Profile.objects.all()
        response = self.client.get(PROFILES_LIST_URL)
        serializer = ProfileSerializer(profiles, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data, serializer.data)

    def test_list_profiles_search_by_user_email(self):
        get_profile(email="qwert@mail.com")
        get_profile(email="user3@mail.com")

        searched_user = Profile.objects.filter(
            user__email__icontains="qwert"
        )
        serializer = ProfileSerializer(searched_user, many=True)
        response = self.client.get(f"{PROFILES_LIST_URL}?email=qwert")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer.data, response.data)

    def test_opens_own_profile(self):
        get_profile(email="user2@mail.com")
        own_profile = Profile.objects.get(user=self.user)
        serializer = ProfileSerializer(own_profile)
        response = self.client.get(PROFILE_OWN_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
