from django.shortcuts import get_object_or_404
from rest_framework import viewsets, filters
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

# from api.permissions import IsOwnerOrReadOnly

from ..reviews.models import Categories, Titles, Genres


class CategoriesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Categories.objects.all()
    # serializer_class = CategoriesSerializer


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Titles.objects.all()
    # serializer_class = TitlesSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
    # pagination_class = LimitOffsetPagination

    # def perform_create(self, serializer):
    #     serializer.save(author=self.request.user)


class GenresViewSet(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    # serializer_class = CommentSerializer
    # permission_classes = (IsOwnerOrReadOnly,)
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
# class CreateListViewSet(mixins.CreateModelMixin,
#                         mixins.ListModelMixin,
#                         viewsets.GenericViewSet):
#     pass
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

