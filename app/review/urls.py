"""
Mapping URLs for reviews
"""
from django.urls import (
    path,
    include
)
from rest_framework.routers import DefaultRouter

from review import views

router = DefaultRouter()
router.register('', views.ReviewViewSet, 'review')
app_name = 'review'

urlpatterns = [
    path('', include(router.urls))
]
