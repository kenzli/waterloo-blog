from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views
from .views import PostDetailView, PostCreateView, PostUpdateView, PostDeleteView

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
    path('register/', views.about, name='about'),
    path('profile/', views.user_profile, name='profile'),
    path('blog_post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('blog_post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('blog_post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('blog_post/new/', PostCreateView.as_view(), name='post-create'),
    path('', views.home_page, name='home'),
]
