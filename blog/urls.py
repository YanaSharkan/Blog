from django.urls import path

from . import views


app_name = 'blog'
urlpatterns = [
    path('', views.PostsView.as_view(), name='posts'),
    path('create/', views.CreatePostView.as_view(), name='create_post'),

]