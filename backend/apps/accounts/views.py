from django.shortcuts import render
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model

User = get_user_model()


class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://127.0.0.1:8000/auth/google/callback/"



class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        
        # Connecter automatiquement un compte social (Google) à un compte existant si l'adresse email est déjà enregistrée ou vice versa
        
       # Si le compte social est déjà lié à un utilisateur, on ne fait rien
        if sociallogin.is_existing:
            return

        # Récupérer l'email fourni par Google
        email = sociallogin.account.extra_data.get('email')
        if not email:
            return

        # On cherche dans la table EmailAddress pour s'assurer que l'email est vérifié avant de lier le compte
        try:
            email_address = EmailAddress.objects.get(email__iexact=email, verified=True)
            user = email_address.user
            sociallogin.connect(request, user)
            
        except EmailAddress.DoesNotExist:
            # Si l'email n'est pas dans EmailAddress, on tente le modèle User
            try:
                user = User.objects.get(email__iexact=email)
                sociallogin.connect(request, user)
            except User.DoesNotExist:
                # Si personne n'est trouvé, un nouveau compte est créé
                pass