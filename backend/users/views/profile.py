import json
from typing import Any

from allauth.account.views import LoginView
from django.http import HttpRequest
from django.urls import reverse
from django.views.decorators.cache import cache_control
from inertia import InertiaResponse, inertia


@cache_control(private=True)
@inertia("Public/Home/Index")
def my_profile_page(request: HttpRequest) -> dict[str, Any]:
    """
    Just a placeholder for a real profile page
    """
    return {}
