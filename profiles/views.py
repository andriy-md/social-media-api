from rest_framework.generics import RetrieveUpdateAPIView

from profiles.models import Profile
from profiles.serializers import ProfileSerializer


class ProfileRetrieveUpdateView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    # queryset = Profile.objects.all()

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    # def retrieve(self, request, *args, **kwargs):
    #     print(self.request.user)
    #     return Profile.objects.get(user=self.request.user)
