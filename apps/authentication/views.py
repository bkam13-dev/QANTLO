from dj_rest_auth.views import LoginView
from dj_rest_auth.registration.views import RegisterView, SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.github.views import GitHubOAuth2Adapter
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialConnectView
from dj_rest_auth.views import PasswordResetView

from apps.authentication.serializers import CustomLoginSerializer, CustomRegisterSerializer
from apps.authentication.throttles import LoginRateThrottle, RegistrationRateThrottle, PasswordResetRateThrottle



class CustomLoginView(LoginView):
    serializer_class = CustomLoginSerializer
    throttle_classes = [LoginRateThrottle]
    
    
class CustomRegisterView(RegisterView):
    serializer_class = CustomRegisterSerializer
    throttle_classes = [RegistrationRateThrottle]
    
    

class CustomPasswordResetView(PasswordResetView):
    throttle_classes = [PasswordResetRateThrottle]
    
    
class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    
class GoogleConnectView(SocialConnectView):
    adapter_class = GoogleOAuth2Adapter


class GitHubLoginView(SocialLoginView):
    adapter_class = GitHubOAuth2Adapter

class GitHubConnectView(SocialConnectView):
    adapter_class = GitHubOAuth2Adapter


class FacebookLoginView(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    
class FacebookConnectView(SocialConnectView):
    adapter_class = FacebookOAuth2Adapter