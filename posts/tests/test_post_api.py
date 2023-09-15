from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from posts.models import Hashtag, Post
from posts.serializers import PostListSerializer
from profiles.models import Profile
from profiles.tests.test_profile_api import get_profile, create_sample_user


POSTS_LIST_URL = reverse("posts:post-list")


def create_sample_post(
            author: Profile,
            text: str = "This is sample post only to test api",
            hashtags: tuple = (),
        ):
    post = Post.objects.create(
        author=author,
        text=text
    )
    for hashtag in hashtags:
        new_hashtag, created = Hashtag.objects.get_or_create(name=hashtag)
        post.hashtags.add(new_hashtag.id)
    return post


class AuthenticatedPostTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_sample_user()
        self.client.force_authenticate(self.user)

    def test_list_posts(self):
        profile = get_profile(email="second_user@aa.com")
        create_sample_post(author=profile)
        create_sample_post(author=profile)
        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        response = self.client.get(POSTS_LIST_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), len(serializer.data))

    def test_filter_by_author(self):
        profile2 = get_profile(email="second_user@aa.com")
        profile3 = get_profile(email="third_user@aa.com")
        create_sample_post(author=profile2)
        create_sample_post(author=profile3)

        searched_posts = Post.objects.filter(
            author__user__email__icontains="third"
        )
        response = self.client.get(f"{POSTS_LIST_URL}?author=third")
        serializer = PostListSerializer(searched_posts, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(len(response.data), len(serializer.data))

    def test_filter_by_tag(self):
        profile2 = get_profile(email="second_user@aa.com")
        create_sample_post(
            author=profile2,
            hashtags=("economy", "history")
        )
        create_sample_post(
            author=profile2,
            hashtags=("history", "sport")
        )
        create_sample_post(
            author=profile2,
            hashtags=("economy", "food")
        )

        searched_query = Post.objects.filter(hashtags__id=1)
        searched_query = searched_query.filter(hashtags__id=2)
        serializer = PostListSerializer(searched_query, many=True)
        response = self.client.get(f"{POSTS_LIST_URL}?hashtag=economy,history")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_get_user_own_posts(self):
        profile1 = Profile.objects.get(user=self.user)
        profile2 = get_profile(email="second_user@mm.com")
        create_sample_post(author=profile1)
        create_sample_post(author=profile1)
        create_sample_post(author=profile2)

        searched_query = Post.objects.filter(author=profile1)
        serializer = PostListSerializer(searched_query, many=True)
        response = self.client.get(f"{POSTS_LIST_URL}my-posts/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data, serializer.data)

    def test_get_followed_posts(self):
        # profile 1 (current user) follows profile 2, but not profile 3
        profile1 = Profile.objects.get(user=self.user)
        profile2 = get_profile(email="second_user@mm.com")
        profile1.follows.add(profile2)
        profile3 = get_profile(email="third_user@mm.com")

        # create_posts
        create_sample_post(author=profile1)
        create_sample_post(author=profile2)
        create_sample_post(author=profile2)
        create_sample_post(author=profile3)

        searched_query = Post.objects.filter(author=profile2)
        serializer = PostListSerializer(searched_query, many=True)
        response = self.client.get(f"{POSTS_LIST_URL}followed/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_post_without_creating_hashtags(self):
        Hashtag.objects.create(name="first")
        Hashtag.objects.create(name="second")
        payload = {
            "hashtags": [
                {"name": "first"},
                {"name": "second"}
            ],
            "text": "Test post via API"
        }
        response = self.client.post(POSTS_LIST_URL, data=payload, format="json")
        created_post = Post.objects.filter(text="Test post via API")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_post.count(), 1)
        self.assertEqual(created_post[0].text, payload["text"])
        self.assertEqual(
            list(created_post[0].hashtags.all()),
            list(Hashtag.objects.all())
        )

    def test_create_post_and_hashtags(self):
        payload = {
            "hashtags": [
                {"name": "first"},
                {"name": "second"}
            ],
            "text": "Test post via API"
        }
        response = self.client.post(POSTS_LIST_URL, data=payload, format="json")
        created_post = Post.objects.filter(text="Test post via API")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_post.count(), 1)
        self.assertEqual(created_post[0].text, payload["text"])
        self.assertEqual(
            list(created_post[0].hashtags.all()),
            list(Hashtag.objects.all())
        )
