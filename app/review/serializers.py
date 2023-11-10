"""
Creating serializers for reviews.
"""
from core.models import Review
from rest_framework import serializers


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",
            "review",
            "rating",
            "date_created",
            "date_updated",
            "book",
        ]
        read_only_fields = ["id"]
