from django.contrib import admin

from posts.models import Post, Hashtag

admin.site.register(Hashtag)
admin.site.register(Post)
