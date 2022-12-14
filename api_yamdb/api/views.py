from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminOrReadOnly
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer)

from ..reviews.models import Categories, Titles, Genres


class CreateListDestroyViewSet(mixins.CreateModelMixin,
                               mixins.ListModelMixin,
                               mixins.DestroyModelMixin,
                               viewsets.GenericViewSet):
    pass


class CategoriesViewSet(CreateListDestroyViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    serializer_class = TitlesSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)

#
#     def get_post(self):
#         return get_object_or_404(Post, id=self.kwargs.get('post_id'))
#
#     def get_queryset(self):
#         return self.get_post().comments
#
#     def perform_create(self, serializer):
#         serializer.save(author=self.request.user,
#                         post=self.get_post())
#
#

#
# class FollowViewSet(CreateListViewSet):
#     serializer_class = FollowSerializer
#     permission_classes = (IsAuthenticated,)
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('following__username',)
#
#     def get_queryset(self):
#         return self.request.user.follower.all()
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
