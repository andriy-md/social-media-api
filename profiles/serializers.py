from rest_framework import serializers

from profiles.models import Profile


class ProfileRetrieveSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    follows = serializers.StringRelatedField(many=True)
    followed_by = serializers.StringRelatedField(many=True)

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "picture", "follows", "followed_by"]


class OwnProfileUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = ["id", "user", "bio", "picture", "follows"]
