from django.db.models import Avg
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import (Categories, Genres, Titles, Comments,
                            Reviews, GenresTitles)


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ('name', 'slug')


class GenresTitlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenresTitles
        fields = ('title', 'genre')


class TitlesSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = CategoriesSerializer(read_only=True)
    genre = GenresSerializer(many=True, read_only=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'genre', 'category')

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(Avg('score'))['score__avg']


class PostTitlesSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='slug')
    genre = GenresSerializer(required=False, many=True,
                             source='slug', read_only=True)

    class Meta:
        model = Titles
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')

    def create(self, validated_data):
        if 'genre' not in self.initial_data:
            title = Titles.objects.create(**validated_data)
            return title
        else:
            genres = validated_data.pop('genre')
            title = Titles.objects.create(**validated_data)
            for genre in genres:
                current_genre = get_object_or_404(Genres, genre=genre)
                GenresTitles.objects.create(
                    genre=current_genre, title=title
                )
            return title


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    # title = serializers.SlugRelatedField(read_only=True, slug_field='name')

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Reviews


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comments
