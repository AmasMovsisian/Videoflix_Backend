from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """Manager for the custom User model with email-based authentication."""

    def create_user(
        self,
        email,
        password=None,
        **extra_fields
    ):
        """Create, save and return a regular user with the given email and password."""
        if not email:
            raise ValueError(
                "Email is required"
            )

        email = self.normalize_email(
            email
        )

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(
            password
        )

        user.save(
            using=self._db
        )

        return user

    def create_superuser(
        self,
        email,
        password=None,
        **extra_fields
    ):
        """Create, save and return a superuser with elevated permissions."""
        extra_fields.setdefault(
            "is_staff",
            True
        )

        extra_fields.setdefault(
            "is_superuser",
            True
        )

        extra_fields.setdefault(
            "is_active",
            True
        )

        return self.create_user(
            email,
            password,
            **extra_fields
        )