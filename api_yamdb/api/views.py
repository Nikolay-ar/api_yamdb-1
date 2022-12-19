from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, filters
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticated
from reviews.models import (Categories, Titles, Genres,
                            Reviews, GenresTitles, Comments)

from .permissions import (IsAdminOrReadOnly,
                          IsAuthorOrIsModeratorOrAdminOrReadOnly)
from .serializers import (CategoriesSerializer,
                          GenresSerializer,
                          TitlesSerializer,
                          CommentSerializer,
                          ReviewSerializer, PostTitlesSerializer)


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
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'slug'
    search_fields = ('name',)


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    filterset_fields = ('name', 'year')

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return PostTitlesSerializer
        return TitlesSerializer

    def get_queryset(self):
        queryset = Titles.objects.all()
        category_slug = self.request.query_params.get('category')
        genre_slug = self.request.query_params.get('genre')
        if category_slug is not None:
            queryset = queryset.filter(
                category=Categories.objects.get(slug=category_slug)
            )
        if genre_slug is not None:
            queryset = queryset.filter(
                genre=Genres.objects.get(slug=genre_slug)
            )
        return queryset


class GenresViewSet(CreateListDestroyViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    lookup_field = 'slug'
    search_fields = ('name',)


class ReviewsViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (IsAuthorOrIsModeratorOrAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Reviews.objects.filter(title=title_id)
        return new_queryset

    @action(detail=False, permission_classes=[IsAuthenticated],
            methods=['post'])
    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        new_queryset = Comments.objects.filter(post=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Titles, id=title_id)
        serializer.save(author=self.request.user, title=title)
