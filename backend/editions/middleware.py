from collections.abc import Callable

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils.translation import gettext_lazy as _


def maintenance_mode(get_response: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    def middleware(request: HttpRequest) -> HttpResponse:
        if settings.ENABLE_MAINTENANCE_MODE:
            message = (
                settings.MAINTENANCE_MESSAGE
                if settings.MAINTENANCE_MESSAGE
                else _("Maintenance window. Sorry for the inconvenience. We will be back soon.")
            )
            return HttpResponse("<!DOCTYPE html><html>" + message + "</html>")

        return get_response(request)

    return middleware
