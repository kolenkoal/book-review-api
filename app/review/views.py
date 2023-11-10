"""
Creating views for the review model.
"""
from core.models import Review
from core.permissions import IsObjectOwner
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from review.serializers import ReviewSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsObjectOwner]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
