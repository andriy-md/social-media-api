from rest_framework import serializers

from posts.models import Post, Hashtag


class HashtagPostCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class PostListSerializer(serializers.ModelSerializer):
    hashtags = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = [
            "id",
            "hashtags",
            "text_preview",
            "author",
            "created_at",
            "updated_at"
        ]


class PostCreateSerializer(serializers.ModelSerializer):
    hashtags = HashtagPostCreateSerializer(many=True)

    class Meta:
        model = Post
        fields = [
            "hashtags",
            "text",
            "created_at",
            "updated_at"
        ]

    def create(self, validated_data):
        hashtags_data = validated_data.pop("hashtags")
        post = Post.objects.create(**validated_data)

        for hashtag in hashtags_data:
            hashtag_to_post, created = Hashtag.objects.get_or_create(
                name=hashtag["name"]
            )
            post.hashtags.add(hashtag_to_post.id)

        return post
