from django.test import TestCase, Client
from .models import Post, User, UserFollowing, UserLike, Comment
# Create your tests here.


class PostTestCase(TestCase):

    def setUp(self):

        # Create two users
        a1 = User.objects.create(username="user1", password="user1")
        a2 = User.objects.create(username="user2", password="user2")
        a3 = User.objects.create(username="user3", password="user3")

        # Create two Posts
        p1 = Post.objects.create(user=a1, content="")
        p2 = Post.objects.create(user=a2, content="p2", like=-1)
        p3 = Post.objects.create(user=a3, content="p3")
    
    # Test for Post Model
    def test_post_count(self):
        u = User.objects.get(username="user2")
        p = Post.objects.filter(user_id=u.id)
        self.assertEqual(p.count(), 1)

    def test_valid_post(self):
        u = User.objects.get(username="user3")
        p = Post.objects.get(user_id=u.id, content="p3")
        self.assertTrue(p.is_valid_post())

    def test_invalid_content_post(self):
        u = User.objects.get(username="user1")
        p = Post.objects.get(user_id=u.id, content="")
        self.assertFalse(p.is_valid_post())

    def test_invalid_like_post(self):
        u = User.objects.get(username="user2")
        p = Post.objects.get(user_id=u.id, content="p2", like=-1)
        self.assertFalse(p.is_valid_post())

    # Test for UserFollowing Model
    def test_valid_follow(self):
        u1 = User.objects.get(username="user1")
        u2 = User.objects.get(username="user2")
        f = UserFollowing(user_id=u1, following_user_id=u2)
        self.assertTrue(f.is_valid_follow())

    def test_invalid_follow(self):
        u1 = User.objects.get(username="user1")
        f = UserFollowing(user_id=u1, following_user_id=u1)
        self.assertFalse(f.is_valid_follow())

    def test_index(self):

        c = Client()

        response = c.get("")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["posts"])

    def test_valid_post_get(self):
        u = User.objects.get(username="user3")
        p = Post.objects.get(user_id=u.id)
        c = Client()
        response = c.get(f"/post/{p.id}")

        self.assertEqual(response.status_code, 202)

    def test_valid_comment(self):
        u = User.objects.get(username="user3")
        p = Post.objects.get(user_id=u.id)
        c = Comment.objects.create(author=u, post=p, comment="Hello")

        self.assertTrue(c.is_valid_comment())

    def test_invalid_comment(self):
        u = User.objects.get(username="user3")
        p = Post.objects.get(user_id=u.id)
        c = Comment.objects.create(author=u, post=p, comment="")

        self.assertFalse(c.is_valid_comment())



