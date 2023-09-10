from django.urls import path

from profiles.views import ManageUserView, ProfileRetrieveUpdateView

urlpatterns = [
    path("me/", ProfileRetrieveUpdateView.as_view()),
    path("me/settings/", ManageUserView.as_view()),
]

app_name = "profile"
