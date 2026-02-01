from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import Post, Like, Comment, Follow
import json

@csrf_exempt
def signup(request):
    data = json.loads(request.body)
    user = User.objects.create_user(
        username=data['username'],
        password=data['password']
    )
    return JsonResponse({"message": "User created"})

@csrf_exempt
def login(request):
    data = json.loads(request.body)
    from django.contrib.auth import authenticate
    user = authenticate(username=data['username'], password=data['password'])
    if user:
        return JsonResponse({"user_id": user.id})
    return JsonResponse({"error": "Invalid credentials"})

@csrf_exempt
def create_post(request):
    data = json.loads(request.body)
    user = User.objects.get(id=data['user_id'])
    Post.objects.create(
        user=user,
        text=data['text'],
        image=data.get('image', "")
    )
    return JsonResponse({"message": "Post created"})

def get_posts(request):
    posts = Post.objects.all().order_by('-created_at')
    data = []
    for post in posts:
        data.append({
            "id": post.id,
            "user": post.user.username,
            "text": post.text,
            "image": post.image,
            "likes": Like.objects.filter(post=post).count(),
        })
    return JsonResponse(data, safe=False)

@csrf_exempt
def like_post(request):
    data = json.loads(request.body)
    user = User.objects.get(id=data['user_id'])
    post = Post.objects.get(id=data['post_id'])
    Like.objects.get_or_create(user=user, post=post)
    return JsonResponse({"message": "Liked"})

@csrf_exempt
def add_comment(request):
    data = json.loads(request.body)
    user = User.objects.get(id=data['user_id'])
    post = Post.objects.get(id=data['post_id'])
    Comment.objects.create(user=user, post=post, text=data['text'])
    return JsonResponse({"message": "Comment added"})

@csrf_exempt
def follow_user(request):
    data = json.loads(request.body)
    follower = User.objects.get(id=data['follower_id'])
    following = User.objects.get(id=data['following_id'])
    Follow.objects.get_or_create(follower=follower, following=following)
    return JsonResponse({"message": "Followed"})
