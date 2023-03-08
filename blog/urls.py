from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('feedback/', views.leave_feedback, name='feedback'),
    path('edit/<int:pk>', views.EditPostView.as_view(), name='edit_post'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.RegisterFormView.as_view(), name='register'),
    path("update_profile/", views.UpdateProfile.as_view(), name="update_profile"),
    path("view_profile/<int:pk>", views.Profile.as_view(), name="profile"),
    path('posts_by_author/<int:author>', views.PostsView.as_view(), name='author_posts'),
    path('<int:pk>/', views.PostView.as_view(), name='post'),
    path('<int:pk>/create_comment', views.CreateCommentView.as_view(), name='create_comment')
]
