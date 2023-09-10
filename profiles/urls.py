from django.urls import path
from rest_framework.routers import DefaultRouter

from profiles.views import ManageUserView, OwnProfileRetrieveUpdateView, ProfileViewSet

router = DefaultRouter()

router.register("", ProfileViewSet)

urlpatterns = [
    path("me/", OwnProfileRetrieveUpdateView.as_view()),
    path("me/settings/", ManageUserView.as_view()),
]

urlpatterns += router.urls

app_name = "profile"
