from typing import Any

from django.http import HttpRequest
from django.views.decorators.cache import cache_control
from inertia import inertia


@cache_control(private=False)
@inertia("Public/Home/Index")
def temp_landing_page(request: HttpRequest) -> dict[str, Any]:
    """
    Just a placeholder for a real landing page
    """
    return {}
