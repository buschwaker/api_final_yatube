from django.urls import path, include
from rest_framework import routers

from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('posts', PostViewSet, basename='post')
router_v1.register('groups', GroupViewSet, basename='group')
router_v1.register('follow', FollowViewSet, basename='follow')
router_v1.register(
    r'posts/(?P<post_id>[^/.]+)/comments', CommentViewSet, basename='comment'
)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include('djoser.urls.jwt')),
]
