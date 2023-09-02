from django.contrib import admin
from .models import User, Post, UserFollowing, UserLike, Comment
# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(UserFollowing)
admin.site.register(UserLike)
admin.site.register(Comment)

