"""
Creating views for authors.
"""
from author.serializers import AuthorSerializer
from core.models import Author
from core.permissions import IsObjectOwner
from rest_framework import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet


class AuthorViewSet(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsObjectOwner]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        """Create a new author."""
        serializer.save(user=self.request.user)
