from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path("user/", include("user.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path("authors/", include("author.urls")),
    path("genres/", include("genres.urls")),
    path("books/", include("book.urls")),
    path("reviews/", include("review.urls")),
]
