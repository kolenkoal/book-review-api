"""
Crating serializers for authors.
"""
from rest_framework import serializers

from core.models import Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'second_name']
        read_only_fields = ['id']
