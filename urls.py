from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup),
    path('login/', views.login),
    path('post/create/', views.create_post),
    path('posts/', views.get_posts),
    path('like/', views.like_post),
    path('comment/', views.add_comment),
    path('follow/', views.follow_user),
]
