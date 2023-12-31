from author import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("", views.AuthorViewSet, basename="authors")
app_name = "authors"

urlpatterns = [path("", include(router.urls))]
