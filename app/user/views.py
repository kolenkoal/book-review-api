from rest_framework import generics

from .serializers import UserSerializer


# Create your views here.


class CreateUserViewSet(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer
