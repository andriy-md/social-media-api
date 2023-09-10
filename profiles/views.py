from rest_framework import generics, mixins
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import GenericViewSet

from profiles.models import Profile
from profiles.serializers import (
    ProfileRetrieveSerializer, OwnProfileUpdateSerializer,
)


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    serializer_class = ProfileRetrieveSerializer
    queryset = Profile.objects.all()


class OwnProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileRetrieveSerializer
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProfileRetrieveSerializer
        return OwnProfileUpdateSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
