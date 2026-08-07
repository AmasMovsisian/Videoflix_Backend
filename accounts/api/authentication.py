from rest_framework_simplejwt.authentication import JWTAuthentication


class CookieJWTAuthentication(JWTAuthentication):
    """JWT authentication that reads the access token from cookies instead of headers."""

    def authenticate(self, request):
        """Authenticate user by validating the access token stored in cookies."""
        access_token = request.COOKIES.get(
            "access_token"
        )

        if not access_token:
            return None

        validated_token = self.get_validated_token(
            access_token
        )

        return (
            self.get_user(validated_token),
            validated_token,
        )