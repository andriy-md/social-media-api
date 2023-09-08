from django.urls import path, include

from posts.views import simple_api_view

urlpatterns = [
    path("", simple_api_view),
]

app_name = "posts"
