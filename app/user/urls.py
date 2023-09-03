from django.urls import path, include

from . import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserViewSet.as_view(), name='create'),
]
