from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from posts.serializers import PostListSerializer, PostCreateSerializer
from profiles.models import Profile


class PostViewSet(ModelViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.prefetch_related(
        "hashtags").select_related("author").all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostCreateSerializer

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=profile)
