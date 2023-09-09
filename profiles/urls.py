from django.urls import path

from profiles.views import ProfileRetrieveUpdateView


urlpatterns = [
    path("  ", ProfileRetrieveUpdateView.as_view())
]

app_name = "profile"
