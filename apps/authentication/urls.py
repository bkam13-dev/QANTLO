




from django.urls import path, include, re_path

from dj_rest_auth.views import LogoutView, PasswordChangeView
from dj_rest_auth.registration.views import VerifyEmailView, ResendEmailVerificationView
from apps.authentication.views import (
    GoogleLoginView,
    GitHubLoginView,
    FacebookLoginView,
)
from apps.authentication.views import CustomLoginView, CustomRegisterView, CustomPasswordResetView



urlpatterns = [
    # path("", include("dj_rest_auth.urls")),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password/reset/", CustomPasswordResetView.as_view(), name="password-reset"),
    path("password/change/", PasswordChangeView.as_view(), name="password-change"),
    path('register/', CustomRegisterView.as_view(), name='rest_register'),
    path("verify-email/", VerifyEmailView.as_view(), name="verify-email"),
    # Renvoyer l'email de vérification
    path("resend-email/", ResendEmailVerificationView.as_view(), name="resend-email"),
    path(
        "social/google/",
        GoogleLoginView.as_view(),
        name="google-login",
    ),

    path(
        "social/github/",
        GitHubLoginView.as_view(),
        name="github-login",
    ),

    path(
        "social/facebook/",
        FacebookLoginView.as_view(),
        name="facebook-login",
    ),
    # path("social/", include("dj_rest_auth.registration.urls"))
]
