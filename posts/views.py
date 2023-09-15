from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
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

    def get_queryset(self):
        queryset = Post.objects.prefetch_related(
            "hashtags").select_related("author").all()

        if self.request.query_params.get("author"):
            query = Q()
            searched_profiles = self.request.query_params["author"]
            searched_profiles = searched_profiles.split(",")
            for profile in searched_profiles:
                query |= Q(author__user__email__icontains=profile)
            queryset = queryset.filter(query)

        if self.request.query_params.get("hashtag"):
            searched_tags = self.request.query_params.get("hashtag")
            searched_tags = searched_tags.split(",")
            for tag in searched_tags:
                queryset = queryset.filter(hashtags__name=tag)

        return queryset

    def perform_create(self, serializer):
        profile = Profile.objects.get(user=self.request.user)
        serializer.save(author=profile)

    @action(detail=False, methods=["get"], url_path="my-posts")
    def my_posts(self, request):
        my_posts = self.get_queryset().filter(author__user=request.user)
        serializer = self.get_serializer(my_posts, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
