from rest_framework import serializers

from api_yamdb.reviews.models import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'
