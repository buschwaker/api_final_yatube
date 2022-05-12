from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from rest_framework import permissions
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Post, Group, Comment, Follow

from api.serializers import (
    PostSerializer, GroupSerializer, CommentSerializer, FollowSerializer
)
from api.mixins import ListCreateViewSet
from api.permissions import NotSelfSubscription


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(PostViewSet, self).perform_update(serializer)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_post(self):
        id_post = self.kwargs.get('post_id')
        post = get_object_or_404(Post, pk=id_post)
        return post

    def get_queryset(self):
        post = self.get_post()
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied('Удаление чужого контента запрещено!')
        instance.delete()

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied('Изменение чужого контента запрещено!')
        super(CommentViewSet, self).perform_update(serializer)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class FollowViewSet(ListCreateViewSet):
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated, NotSelfSubscription,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('^following__username',)

    def get_queryset(self):
        user = self.request.user
        return Follow.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
