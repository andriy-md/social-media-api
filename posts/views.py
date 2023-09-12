from rest_framework.viewsets import ModelViewSet

from posts.models import Post
from posts.serializers import PostListSerializer


class PostViewSet(ModelViewSet):
    serializer_class = PostListSerializer
    queryset = Post.objects.prefetch_related("hashtags").select_related("author").all()
