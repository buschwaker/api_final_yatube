from django.contrib import admin

from posts.models import Follow, Post, Group, Comment

admin.site.register(Follow)
admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Comment)
