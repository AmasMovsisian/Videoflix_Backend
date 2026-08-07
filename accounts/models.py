from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model using email as the unique identifier."""

    email = models.EmailField(
        unique=True
    )

    is_active = models.BooleanField(
        default=False
    )

    is_staff = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        default=timezone.now
    )

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """Return the string representation (email) of the user."""
        return self.email