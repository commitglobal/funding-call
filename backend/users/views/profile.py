from typing import Any

from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse
from django.views.decorators.cache import cache_control
from inertia import inertia


@cache_control(private=True)
@inertia("Users/Profile/Index")
def my_profile_page(request: HttpRequest) -> HttpResponseRedirect | dict[str, Any]:
    """
    Just a placeholder for a real profile page
    """
    if not request.user.is_authenticated:
        return redirect(reverse("users-auth:login"))

    return {}
