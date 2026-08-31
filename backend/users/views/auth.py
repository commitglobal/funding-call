import json
from typing import Any

from allauth.account import app_settings as allauth_settings
from allauth.account.internal.decorators import login_not_required
from allauth.account.internal.stagekit import (
    get_pending_stage,
    redirect_to_pending_stage,
)
from allauth.account.utils import get_login_redirect_url
from allauth.account.views import LoginView
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from inertia import InertiaResponse


class InertiaRedirectAuthenticatedUserMixin:
    @method_decorator(login_not_required)
    @method_decorator(never_cache)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any):
        if allauth_settings.AUTHENTICATED_LOGIN_REDIRECTS:
            if request.user.is_authenticated:
                redirect_to = self.get_authenticated_redirect_url()
                return redirect(redirect_to)
            else:
                stage = get_pending_stage(request)
                if stage and stage.is_resumable(request):
                    return redirect_to_pending_stage(request, stage)
        response = super().dispatch(request, *args, **kwargs)  # type:ignore[misc]
        return response

    def get_authenticated_redirect_url(self):
        redirect_field_name = getattr(self, "redirect_field_name", REDIRECT_FIELD_NAME)
        url = None
        if hasattr(self, "get_success_url"):
            try:
                url = self.get_success_url()
            except ImproperlyConfigured:
                # If a view does not provide a `success_url`, Django raises a
                # "No URL to redirect to. Provide a success_url." exception.
                # That is no issue in our case.
                pass
        return get_login_redirect_url(
            self.request,
            url=url,
            redirect_field_name=redirect_field_name,
        )


class FundingLoginView(InertiaRedirectAuthenticatedUserMixin, LoginView):
    def get(self, request):
        return InertiaResponse(
            request,
            "Auth/Login/Index",
            props={
                "class_view": True,
            },
        )

    def get_form_kwargs(self) -> dict:
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        if self.request.method in ("POST", "PUT"):
            kwargs.update(
                {
                    "data": json.loads(self.request.body),
                    "files": self.request.FILES,
                }
            )
        return kwargs

    def get_success_url(self):
        return reverse("users-profiles:my-profile")

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form, **kwargs):
        return InertiaResponse(self.request, "Auth/Login/Index", props={"valid": False})

    def form_valid(self, form):
        return super().form_valid(form)
