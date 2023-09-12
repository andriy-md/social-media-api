from rest_framework import generics, mixins
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.viewsets import GenericViewSet

from profiles.models import Profile
from profiles.serializers import (
    ProfileSerializer, OwnProfileUpdateSerializer,
)


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        queryset = Profile.objects.all()
        if self.request.query_params.get("email", False):
            target = self.request.query_params["email"]
            print(target)
            queryset = queryset.filter(user__email__icontains=target)
        return queryset


class OwnProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return ProfileSerializer
        return OwnProfileUpdateSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)
