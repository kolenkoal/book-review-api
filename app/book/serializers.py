"""
Creating serializers for a book model.
"""
from author.serializers import AuthorSerializer
from core.models import Author, Book, Genre
from genres.serializers import GenreSerializer
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(many=True, required=True)
    genres = GenreSerializer(many=True, required=True)

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "total_pages",
            "published_date",
            "author",
            "genres",
        ]
        read_only_fields = ["id"]

    def _get_or_create_genres(self, genres, book):
        """Handle getting or creating genres as needed."""
        auth_user = self.context["request"].user
        for genre in genres:
            genre_obj, created = Genre.objects.get_or_create(
                user=auth_user, **genre
            )
            book.genres.add(genre_obj)

    def _get_or_create_authors(self, authors, book):
        """Handle getting or creating authors as needed."""
        auth_user = self.context["request"].user
        for author in authors:
            author_obj, created = Author.objects.get_or_create(
                user=auth_user, **author
            )
            book.author.add(author_obj)

    def create(self, validated_data):
        """Create a recipe."""
        authors = validated_data.pop("author", [])
        genres = validated_data.pop("genres", [])
        book = Book.objects.create(**validated_data)
        self._get_or_create_authors(authors, book)
        self._get_or_create_genres(genres, book)

        return book

    def update(self, instance, validated_data):
        """Update recipe."""
        authors = validated_data.pop("author", None)
        genres = validated_data.pop("genres", None)
        if authors is not None:
            instance.author.clear()
            self._get_or_create_authors(authors, instance)

        if genres is not None:
            instance.genres.clear()
            self._get_or_create_genres(genres, instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
