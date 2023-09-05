"""
Mapping URLs genres
"""
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter

from genres import views

router = DefaultRouter()
router.register('', views.GenreViewSet, basename='genre')
app_name = 'genre'

urlpatterns = [
    path('', include(router.urls))
]
