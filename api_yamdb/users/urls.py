from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, confirmation_view, signup_view

app_name = 'users'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet)

urlpatterns = [
    path('auth/signup/', signup_view),
    path('auth/token/', confirmation_view),
    path('', include(router_v1.urls)),
]