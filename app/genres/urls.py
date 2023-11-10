"""
Mapping URLs genres
"""
from django.urls import include, path
from genres import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("", views.GenreViewSet, basename="genre")
app_name = "genre"

urlpatterns = [path("", include(router.urls))]
