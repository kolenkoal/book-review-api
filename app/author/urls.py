from django.urls import (
    path,
    include
)

from rest_framework.routers import DefaultRouter

from author import views

router = DefaultRouter()
router.register('', views.AuthorViewSet, basename='authors')
app_name = 'authors'

urlpatterns = [
    path('', include(router.urls))
]
