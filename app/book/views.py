"""
Defining views for genres.
"""
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from core.models import Book
from book.serializers import BookSerializer


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """Create a new book."""
        serializer.save(user=self.request.user)

    def _params_to_ints(self, qs):
        """Convert a list of strings to integers."""
        return [int(str_id) for str_id in qs.split(',')]

    def get_queryset(self):
        """Retrieve genres for authenticated user."""
        genres = self.request.query_params.get('genres')
        authors = self.request.query_params.get('author')
        queryset = self.queryset
        if genres:
            genre_ids = self._params_to_ints(genres)
            queryset = queryset.filter(genres__id__in=genre_ids)

        if authors:
            author_ids = self._params_to_ints(authors)
            queryset = queryset.filter(author__id__in=author_ids)

        return queryset.filter(
            user=self.request.user
        ).order_by('-id').distinct()
