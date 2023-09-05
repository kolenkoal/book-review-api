"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError("Email must be specified.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Author(models.Model):
    """A model for n author in the system."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    first_name = models.CharField(max_length=255)
    second_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.first_name} {self.second_name}'


class Genre(models.Model):
    """A model for a genre in the system."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """A model for a book in the system."""
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    total_pages = models.IntegerField()
    author = models.ManyToManyField(Author)
    published_date = models.DateField()
    genres = models.ManyToManyField(Genre)
