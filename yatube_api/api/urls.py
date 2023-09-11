from django.urls import include, path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views


from .views import PostViewSet


router = SimpleRouter()
router.register('posts', PostViewSet, basename='posts')  # получаем список всех постов или создаём новый пост


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
