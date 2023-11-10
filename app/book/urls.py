"""
Mapping URLs genres
"""
from book import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("", views.BookViewSet, basename="book")
app_name = "book"

urlpatterns = [path("", include(router.urls))]
