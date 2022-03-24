from django.urls import path
from .import views
from .views import (PostListView,create_post_view,PostDetailView,PostUpdateView,PostDeleteView,
	CommentDeleteView,UserPostListView,ConsoleListView,PostLikeView,CommentLikeView,GetLikedPosts,UserPostComView)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
	path('', views.home, name='home-page'),
	path('posts/new/',create_post_view, name = 'create-post'),
	path('posts/',PostListView,name = 'post-list'),
	path('<str:username>/<slug:slug>/',PostDetailView, name = 'post-detail'),
	path('<str:username>/<slug:slug>/update/',PostUpdateView, name = 'post-update'),
	path('<str:username>/<slug:slug>/delete/',PostDeleteView.as_view(), name = 'post-delete'),
	path('<str:username>/<slug:slug>/<str:commenter>/<int:comment_id>/',CommentDeleteView, name = 'comment-delete'),
	path('posts/console-posts/<str:game_console>/',ConsoleListView, name = 'console-post'),
	path('posts/user-posts/<str:username>/',UserPostListView, name = 'user-post-list'),
	path('<str:username>/<slug:slug>/postlikes/',PostLikeView, name = 'post-like'),
	path('<str:username>/<slug:slug>/<int:comment_id>/commentlikes', CommentLikeView, name="comment-like"),
	path("posts/liked-posts/<str:username>/",GetLikedPosts,name = "liked-posts"),
	path('posts/user-posts/<str:username>/posts-commented-on',UserPostComView, name = "post-user-com"),
			
]

