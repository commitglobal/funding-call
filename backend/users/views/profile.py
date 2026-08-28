from typing import Any

from django.http import HttpRequest
from django.views.decorators.cache import cache_control
from inertia import inertia


@cache_control(private=True)
@inertia("Public/Home/Index")
def my_profile_page(request: HttpRequest) -> dict[str, Any]:
    """
    Just a placeholder for a real profile page
    """
    return {}
