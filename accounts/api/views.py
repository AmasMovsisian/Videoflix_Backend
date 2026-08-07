from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)
from django.contrib.auth import authenticate
from django.conf import settings
from django.core.mail import send_mail

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User

from .serializers import RegisterSerializer
from accounts.utils import send_activation_email
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class RegisterView(APIView):
    """API endpoint for user registration."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST request to register a new user and send activation email."""
        serializer = RegisterSerializer(
            data=request.data
        )

        if serializer.is_valid():

            user = serializer.save()

            token = send_activation_email(
                user
            )

            return Response(
                {
                    "user": {
                        "id": user.id,
                        "email": user.email,
                    },
                    "token": token,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class ActivateAccountView(APIView):
    """API endpoint to activate a user account via token from email."""

    permission_classes = [AllowAny]

    def get(
        self,
        request,
        uidb64,
        token,
    ):
        """Handle GET request to verify activation token and activate the user."""
        try:
            uid = force_str(
                urlsafe_base64_decode(uidb64)
            )

            user = User.objects.get(
                pk=uid
            )

        except User.DoesNotExist:

            return Response(
                {
                    "message": "Activation failed."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if default_token_generator.check_token(
            user,
            token
        ):

            user.is_active = True
            user.save()

            return Response(
                {
                    "message": "Account successfully activated."
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "message": "Activation failed."
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(APIView):
    """API endpoint for user login, returning JWT tokens via cookies."""

    permission_classes = [AllowAny]

    def post(
        self,
        request,
    ):
        """Handle POST request to authenticate user and set access/refresh cookies."""
        email = request.data.get(
            "email"
        )

        password = request.data.get(
            "password"
        )

        user = authenticate(
            request,
            username=email,
            password=password,
        )

        if user is None:

            return Response(
                {
                    "detail": "Invalid credentials."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(
            user
        )

        response = Response(
            {
                "detail": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.email,
                },
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        return response


class RefreshTokenView(APIView):
    """API endpoint to refresh the access token using a valid refresh token cookie."""

    permission_classes = [AllowAny]

    def post(
        self,
        request,
    ):
        """Handle POST request to issue a new access token from the refresh token."""
        refresh_token = request.COOKIES.get(
            "refresh_token"
        )

        if not refresh_token:

            return Response(
                {
                    "detail": "Refresh token missing."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:

            refresh = RefreshToken(
                refresh_token
            )

            access_token = refresh.access_token

            response = Response(
                {
                    "detail": "Token refreshed successfully."
                },
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                key="access_token",
                value=str(access_token),
                httponly=True,
                secure=False,
                samesite="Lax",
            )

            return response

        except Exception:

            return Response(
                {
                    "detail": "Invalid refresh token."
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )


class LogoutView(APIView):
    """API endpoint to blacklist the refresh token and clear auth cookies."""

    permission_classes = [
        AllowAny
    ]

    def post(self, request):
        """Handle POST request to logout user by invalidating the refresh token."""
        refresh_token = request.COOKIES.get(
            "refresh_token"
        )

        if refresh_token:

            try:
                token = RefreshToken(
                    refresh_token
                )

                token.blacklist()

            except Exception:
                pass

        response = Response(
            {
                "detail": "Logout successful! All tokens will be deleted. Refresh token is now invalid."
            },
            status=status.HTTP_200_OK,
        )

        response.delete_cookie(
            "access_token"
        )

        response.delete_cookie(
            "refresh_token"
        )

        return response


class PasswordResetRequestView(APIView):
    """API endpoint to request a password reset link via email."""

    permission_classes = [AllowAny]

    def post(
        self,
        request,
    ):
        """Handle POST request to generate token and send password reset email."""
        email = request.data.get(
            "email"
        )

        try:

            user = User.objects.get(
                email=email
            )

        except User.DoesNotExist:

            return Response(
                {
                    "message": "An email has been sent to reset your password."
                },
                status=status.HTTP_200_OK,
            )

        uid = urlsafe_base64_encode(
            force_bytes(user.pk)
        )

        token = default_token_generator.make_token(
            user
        )

        reset_url = (
            f"{settings.FRONTEND_URL}"
            f"/reset-password/"
            f"{uid}/"
            f"{token}/"
        )

        send_mail(
            subject="Reset your Videoflix password",
            message=(
                "Reset your password here:\n\n"
                f"{reset_url}"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response(
            {
                "message": "An email has been sent to reset your password."
            },
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(APIView):
    """API endpoint to confirm password reset with token and set a new password."""

    permission_classes = [AllowAny]

    def post(self, request):
        """Handle POST request to validate token and update the user's password."""
        uid = request.data.get("uid")
        token = request.data.get("token")
        password = request.data.get("password")
        confirmed_password = request.data.get("confirmed_password")

        if password != confirmed_password:
            return Response(
                {
                    "message": "Passwords do not match."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_id = force_str(
                urlsafe_base64_decode(uid)
            )

            user = User.objects.get(
                pk=user_id
            )

        except User.DoesNotExist:
            return Response(
                {
                    "message": "Invalid user."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not default_token_generator.check_token(
            user,
            token
        ):
            return Response(
                {
                    "message": "Invalid or expired token."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(
                password,
                user
            )

        except ValidationError as e:
            return Response(
                {
                    "message": e.messages
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.set_password(
            password
        )

        user.save()

        return Response(
            {
                "message": "Your Password has been successfully reset."
            },
            status=status.HTTP_200_OK
        )
