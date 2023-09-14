from django.db import models

from profiles.models import Profile


class Hashtag(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    hashtags = models.ManyToManyField(
        Hashtag,
        related_name="posts",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def text_preview(self):
        if len(self.text) < 32:
            return self.text
        return self.text[:31]

    def __str__(self):
        return f'"{self.text_preview}" by {self.author}'
