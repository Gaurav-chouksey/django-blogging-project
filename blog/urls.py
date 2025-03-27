from django.urls import path, include
from .views import post_list, post_detail, signup, post_create, add_comment, PostViewSet, CommentViewSet, profile, post_update, post_delete, comment_update, comment_delete, post_like, comment_like
from rest_framework.routers import DefaultRouter
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)

urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/new/', post_create, name='post_create'),
    path('post/<int:pk>/edit/', post_update, name='post_update'),
    path('post/<int:pk>/delete/', post_delete, name='post_delete'),
    path('post/<int:pk>/comment/', add_comment, name='add_comment'),
    path('comment/<int:pk>/edit/', comment_update, name='comment_update'),
    path('comment/<int:pk>/delete/', comment_delete, name='comment_delete'),
    path('post/<int:pk>/like/', post_like, name='post_like'),
    path('comment/<int:pk>/like/', comment_like, name='comment_like'),
    path('signup/', signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='post_list'), name='logout'),
    path('profile/', profile, name='profile'),
]
