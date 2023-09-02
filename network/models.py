from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="poster")
    content = models.TextField(max_length=180, null=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.IntegerField(default=0)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.user.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p"),
            "like": self.like
        }

    def __str__(self):
        return f"Post {self.id}: {self.user} - {self.content} - {self.timestamp} - Likes: {self.like}"

    def is_valid_post(self):
        return self.like >= 0 and self.content != ""

class UserFollowing(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"
    
    def is_valid_follow(self):
        return self.user_id != self.following_user_id

class UserLike(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_like")
    post_like = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_like")

    def __str__(self):
        return f"{self.user_id} liked {self.post_like}"
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="author")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comment")
    timedate = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=180, null=False)

    def __str__(self):
        return f"{self.author} comment {self.comment} in post {self.post.id}"
    
    def is_valid_comment(self):
        return self.comment != ""