from django.urls import path
from rest_framework.routers import DefaultRouter

from profiles.views import OwnProfileRetrieveUpdateView, ProfileViewSet

router = DefaultRouter()

router.register("", ProfileViewSet)

urlpatterns = [
    path("me/", OwnProfileRetrieveUpdateView.as_view(), name="my-profile"),
]

urlpatterns += router.urls

app_name = "profile"
