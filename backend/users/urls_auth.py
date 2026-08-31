"""
User authentication URLs for both regular members and staff members
"""

from django.urls import include, path

from .views.auth import FundingLoginView

app_name = "users-auth"
urlpatterns = [
    path("login/", FundingLoginView.as_view(), name="login"),
    #
    # TODO: replace the remaining URLs
    path("", include("allauth.urls")),
]
