from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def create_activation_token(user):
    """Generate and return an activation token for the given user."""
    return default_token_generator.make_token(user)


def create_activation_url(user, token):
    """Build activation URL for the frontend."""

    uid = urlsafe_base64_encode(
        force_bytes(user.pk)
    )

    return (
        f"{settings.FRONTEND_URL}/pages/auth/activate.html"
        f"?uid={uid}&token={token}"
    )


def send_activation_email(user):
    """Send a multipart activation email to the user and return the generated token."""
    token = create_activation_token(
        user
    )

    activation_url = create_activation_url(
        user,
        token,
    )

    context = {
        "user": user,
        "activation_url": activation_url,
    }

    text_content = render_to_string(
        "emails/activation.txt",
        context,
    )

    html_content = render_to_string(
        "emails/activation.html",
        context,
    )

    email = EmailMultiAlternatives(
        subject="Activate your Videoflix account",
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[
            user.email,
        ],
    )

    email.attach_alternative(
        html_content,
        "text/html",
    )

    email.send()

    return token