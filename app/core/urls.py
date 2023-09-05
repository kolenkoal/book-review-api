from django.urls import (
    path,
    include
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import (
    DefaultRouter
)

from author import views

router = DefaultRouter()
router.register(r'authors', views.AuthorViewSet, basename='authors')

urlpatterns = [
    path('user/', include('user.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path(
        'docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs'
    ),
    path('', include(router.urls))
]
