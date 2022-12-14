from django.urls import path, include
from rest_framework import routers

from .views import TitlesViewSet, CategoriesViewSet, GenresViewSet

router_v1 = routers.DefaultRouter()
router_v1.register(r'titles', TitlesViewSet, basename='titles')
router_v1.register(r'categories', CategoriesViewSet, basename='categories')
# router_v1.register(r'categories/{slug}', GroupViewSet, basename='groups')
router_v1.register(r'genres', GenresViewSet, basename='genres')
# router_v1.register(r'genres/{slug}', GenresViewSet, basename='genres')


urlpatterns = [
    path('', include(router_v1.urls)),
    # path('v1/', include('djoser.urls.jwt')),
]
