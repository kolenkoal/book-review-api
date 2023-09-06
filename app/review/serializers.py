"""
Creating serializers for reviews.
"""
from rest_framework import serializers

from core.models import Review


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'review', 'rating', 'date_created', 'date_updated',
                  'book']
        read_only_fields = ['id']
