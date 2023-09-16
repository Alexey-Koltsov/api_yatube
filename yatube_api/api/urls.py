from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from .views import CommentViewSet, GroupViewSet, PostViewSet


posts_01api_router = routers.DefaultRouter()
posts_01api_router.register('posts', PostViewSet, basename='posts')
posts_01api_router.register('groups', GroupViewSet, basename='groups')
posts_01api_router.register(r'posts/(?P<post_id>\d+)/comments',
                            CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(posts_01api_router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
