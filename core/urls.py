from django.urls import path # type: ignore
from core import views # type: ignore

urlpatterns = [
    path('', views.home_view, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('create-post/', views.create_post_view, name='create_post'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('users/', views.users_view, name='users'),
    path('profile/', views.profile_view, name='my_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    path('follow/<int:profile_id>/', views.toggle_follow, name='toggle_follow'),
]
