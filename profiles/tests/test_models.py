from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from profiles.models import Profile


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


class ProfileModelTest(TestCase):
    def setUp(self):
        self.profile1 = get_profile()

    def test_profile_creates_when_user_created(self):
        user1 = create_sample_user(email="user2@mail.com")
        profile1 = Profile.objects.filter(user=user1)
        self.assertEqual(profile1.count(), 1)
        self.assertEqual(profile1.first().user, user1)

    def test_profile_can_follow_many_other_profiles(self):
        profile2 = get_profile(email="user2@mail.com")
        profile3 = get_profile(email="user3@mail.com")

        self.profile1.follows.add(profile2, profile3)

        self.assertEqual(self.profile1.follows.count(), 2)
        self.assertIn(profile2, list(self.profile1.follows.all()))
        self.assertIn(profile3, list(self.profile1.follows.all()))

    def test_profile_can_be_followed_by_many_other_profiles(self):
        profile2 = get_profile(email="user2@mail.com")
        profile3 = get_profile(email="user3@mail.com")
        profile2.follows.add(self.profile1)
        profile3.follows.add(self.profile1)

        self.assertEqual(self.profile1.followed_by.count(), 2)

    def test_profile_follow_is_not_symmetrical(self):
        profile2 = get_profile(email="user2@mail.com")
        self.profile1.follows.add(profile2)

        self.assertEqual(self.profile1.follows.count(), 1)
        self.assertEqual(profile2.follows.count(), 0)

    def test_profile_deletes_if_user_is_deleted(self):
        user = get_user_model().objects.get(email="test_user@test.com")
        user.delete()

        with self.assertRaises(ObjectDoesNotExist):
            self.profile1.refresh_from_db()
