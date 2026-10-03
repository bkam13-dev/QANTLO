


from django.urls import path
from apps.users.views import CurrentUserProfileView, CurrentUserView, DeleteAccountView

urlpatterns = [
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("me/profile/", CurrentUserProfileView.as_view(), name="current-user-profile"),
    path("me/delete/", DeleteAccountView.as_view(), name="delete-account"),
]
