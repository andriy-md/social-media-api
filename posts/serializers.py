from rest_framework import serializers

from posts.models import Post


class PostListSerializer(serializers.ModelSerializer):
    hashtags = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = [
            "hashtags",
            "text_preview",
            "author",
            "created_at",
            "updated_at"
        ]
