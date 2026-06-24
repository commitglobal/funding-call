from typing import Any

from django.views.decorators.cache import cache_control
from django.http import HttpRequest
from inertia import inertia


@cache_control(private=False)
@inertia("Public/Home/Index")
def test(request: HttpRequest) -> dict[str, Any]:
    """
    Just a test view
    """
    return {}

