from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, UserFollowing, UserLike, Comment


def index(request):
    if request.method == "POST":
        content = request.POST["newPost"]
        if content == "":
            return HttpResponseRedirect(reverse("index"))
        
        post = Post.objects.create(user_id=request.user.id, content=content)
        post.save()

        # For pagination
        all_posts = Post.objects.all().order_by("-timestamp")
        posts = [] 
        for i in range(0, len(all_posts)):
            posts.append(all_posts[i])
        posts.sort(key=lambda post: post.id, reverse=True)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        # For likes
        likes = UserLike.objects.filter(user_id=request.user.id)
        liked_posts = []
        for i in range(0, len(likes)):
            for j in range(0, len(posts)):
                if likes[i].post_like == posts[j]:
                    liked_posts.append(posts[j])

        return render(request, "network/index.html", 
                  {"posts": page_obj,
                   "likes": liked_posts})

    
    # For pagination
    all_posts = Post.objects.all().order_by("-timestamp")
    posts = [] 
    for i in range(0, len(all_posts)):
        posts.append(all_posts[i])
    posts.sort(key=lambda post: post.id, reverse=True)
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    # For likes
    likes = UserLike.objects.filter(user_id=request.user.id)
    liked_posts = []
    for i in range(0, len(likes)):
        for j in range(0, len(posts)):
            if likes[i].post_like == posts[j]:
                liked_posts.append(posts[j])

    return render(request, "network/index.html", 
                  {"posts": page_obj,
                   "likes": liked_posts,
                   })

def addComment(request, post_id):
    if request.method == "POST":
        comment = request.POST["comment"]
        post = Post.objects.get(pk=post_id)
        if comment == "":
            comments = Comment.objects.filter(post_id=post_id)
            comment_list = []
            for i in range(0, len(comments)):
                comment_list.append(comments[i])
            comment_list.sort(key=lambda comment: comment.id, reverse=True)        

            # For likes of the POST
            likes = UserLike.objects.filter(user_id=request.user.id)
            like_post = []
            for i in range(0, len(likes)):
                like_post.append(likes[i].post_like)
            if post in like_post:
                likes = "Yes"
            else:
                likes = "Not"

            return render(request, "network/post.html", {
                "post": post,
                "comments": comment_list,
                "likes": likes,
                "message": "Error: Empty Comment"})
        else:
            newComment = Comment.objects.create(author=request.user, post=post, comment=comment)
            newComment.save()
            return HttpResponseRedirect(reverse("post_page", args=[post.id]))

@csrf_exempt
def post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post Not Found"}, status=404)
    
    if request.method == "GET":
        return JsonResponse(post.serialize(), status=202)
        
    
    # To update a post or give a like
    elif request.method == "PUT":
        data = json.loads(request.body)
        try:
            post.content = data["content"]
            post.save()
            return HttpResponse(status=204)
        except KeyError:
            try:
                like = UserLike.objects.get(user_id=request.user.id, post_like=post_id)
            except UserLike.DoesNotExist:
                like = UserLike.objects.create(user_id=request.user, post_like=post)
            if post.like > data["like"]:
                like.delete()
                post.like = data["like"]
                post.save()
            else:
                post.like = data["like"]
                post.save()
            return HttpResponse(status=204)
        
    # Email must be via GET or PUT
    else:
        return JsonResponse({
            "error": "GET or PUT request required."
        }, status=400)



@csrf_exempt
def post_page(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post Not Found"}, status=404)
    
    if request.method == "GET":
        comments = Comment.objects.filter(post_id=post_id)
        comment_list = []
        for i in range(0, len(comments)):
            comment_list.append(comments[i])
        comment_list.sort(key=lambda comment: comment.id, reverse=True)        

        # For likes of the POST
        likes = UserLike.objects.filter(user_id=request.user.id)
        like_post = []
        for i in range(0, len(likes)):
            like_post.append(likes[i].post_like)
        if post in like_post:
            likes = "Yes"
        else:
            likes = "Not"

        return render(request, "network/post.html", {
            "post": post,
            "comments": comment_list,
            "likes": likes})
        
@csrf_exempt
def profile(request, profile):
    if request.method == "POST":
        data = json.loads(request.body)
        act = data["f"]
        if act == "Follow":
            user = User.objects.get(id=request.user.id)
            follow_user = User.objects.get(username=profile)
            UserFollowing.objects.create(user_id=user, following_user_id=follow_user)
            return HttpResponse(status=204)
        
        elif act == "Unfollow":
            user = User.objects.get(id=request.user.id)
            follow_user = User.objects.get(username=profile)
            UserFollowing.objects.get(user_id=user, following_user_id=follow_user).delete()
            return HttpResponse(status=204)

    # GET METHOD
    try:
        f = UserFollowing.objects.get(user_id=User.objects.get(id=request.user.id), following_user_id=User.objects.get(username=profile))
        status = "Followed"
        # Ordered posts by id
        all_posts = Post.objects.filter(user=User.objects.get(username=profile)).order_by('-timestamp').all()
        posts = [] 
        for i in range(0, len(all_posts)):
            posts.append(all_posts[i])
        posts.sort(key=lambda post: post.id, reverse=True)

        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        likes = UserLike.objects.filter(user_id=request.user.id)
        liked_posts = []
        for i in range(0, len(likes)):
            for j in range(0, len(posts)):
                if likes[i].post_like == posts[j]:
                    liked_posts.append(posts[j])

        followers = 0
        following = 0
        for i in range(0, len(UserFollowing.objects.filter(following_user_id=User.objects.get(username=profile)))):
            followers += 1

        for j in range(0, len(UserFollowing.objects.filter(user_id=User.objects.get(username=profile)))):
            following += 1

        return render(request, "network/profile.html", 
                    {"posts": page_obj,
                    "name": profile,
                    "status": status,
                    "likes": liked_posts,
                    "following": following,
                    "followers": followers,
                    })
                    
    except ObjectDoesNotExist:
        status = "Not"
        all_posts = Post.objects.filter(user=User.objects.get(username=profile)).order_by('-timestamp').all()
        posts = [] 
        for i in range(0, len(all_posts)):
            posts.append(all_posts[i])
        posts.sort(key=lambda post: post.id, reverse=True)
        paginator = Paginator(posts, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        likes = UserLike.objects.filter(user_id=request.user.id)
        liked_posts = []
        for i in range(0, len(likes)):
            for j in range(0, len(posts)):
                if likes[i].post_like == posts[j]:
                    liked_posts.append(posts[j])
        
        followers = 0
        following = 0
        for i in range(0, len(UserFollowing.objects.filter(following_user_id=User.objects.get(username=profile)))):
            followers += 1

        for j in range(0, len(UserFollowing.objects.filter(user_id=User.objects.get(username=profile)))):
            following += 1

        return render(request, "network/profile.html", 
                    {"posts": page_obj,
                    "name": profile,
                    "status": status,
                    "likes": liked_posts,
                    "followers": followers,
                    "following": following,
                    })


def following(request):
    # QuerySet, the users that the logged in user follows
    # <QuerySet [<UserFollowing: carlos follows alschz>, <UserFollowing: carlos follows alfonso>]>
    following_ = UserFollowing.objects.filter(user_id=User.objects.get(id=request.user.id))

    # List with the users that follow
    iFollow = []    #[<User: alschz>, <User: alfonso>]
    for i in range(0, len(following_)):
        iFollow.append(following_[i].following_user_id)

    #list with the querySet of posts 
    posts = []  # Two QuerySets
    for i in range(0, len(iFollow)):
        posts.append(Post.objects.filter(user=iFollow[i]))

    posts_query = []
    for i in range(0, len(posts)):  #for every queryset
        for k in range(0, len(posts[i])):   #for every post inside a queryset
            posts_query.append(posts[i][k])

    # Sort by id post with a lambda function
    posts_query.sort(key=lambda post: post.id, reverse=True)
    
    # For pagination
    paginator = Paginator(posts_query, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    likes = UserLike.objects.filter(user_id=request.user.id)
    liked_posts = []
    for i in range(0, len(likes)):
        for j in range(0, len(posts_query)):
            if likes[i].post_like == posts_query[j]:            
                liked_posts.append(posts_query[j])
    
    return render(request, "network/following.html",
                  {
                   "posts":page_obj,
                   "likes":liked_posts,
                   })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
