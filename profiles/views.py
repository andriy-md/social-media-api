from rest_framework import generics
from rest_framework.generics import RetrieveUpdateAPIView

from profiles.models import Profile
from profiles.serializers import (
    OwnProfileRetrieveSerializer, OwnProfileUpdateSerializer,
)
from users.serializers import UserSerializer


class ProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = OwnProfileRetrieveSerializer
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.request.method == "GET":
            return OwnProfileRetrieveSerializer
        return OwnProfileUpdateSerializer

    def get_object(self):
        return Profile.objects.get(user=self.request.user)


class ManageUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

