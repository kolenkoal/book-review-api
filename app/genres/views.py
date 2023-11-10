"""
Defining views for genres.
"""
from core.models import Genre
from core.permissions import IsObjectOwner
from genres.serializers import GenreSerializer
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet


class GenreViewSet(ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsObjectOwner]

    def perform_create(self, serializer):
        """Create a new genre."""
        serializer.save(user=self.request.user)
