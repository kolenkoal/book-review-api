"""
Creating serializers for authors.
"""
from core.models import Author
from rest_framework import serializers


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ["id", "first_name", "second_name"]
        read_only_fields = ["id"]
