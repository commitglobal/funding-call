"""
User authentication URLs for both regular members and staff members
"""

from django.urls import path

from .views.profile import my_profile_page

app_name = "users-profiles"
urlpatterns = [
    path("", my_profile_page, name="my-profile"),
]
