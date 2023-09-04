
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:profile>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("addComment/<int:post_id>", views.addComment, name="comment"),
    path("postPage/<int:post_id>", views.post_page, name="post_page"),

    # API Route
    path("post/<int:post_id>", views.post, name="post"),
    path("profile/post/<int:post_id>", views.post, name="post_profile"),
    path("post_page/post/<int:post_id>", views.post, name="post_post"),
    path("postPage/post/<int:post_id>", views.post, name="postPage_post")
]
