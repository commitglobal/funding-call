import json
from typing import Any

from allauth.account.views import LoginView
from django.http import HttpRequest
from django.urls import reverse
from django.views.decorators.cache import cache_control
from inertia import InertiaResponse, inertia


class FundingLoginView(LoginView):
    def get(self, request):
        return InertiaResponse(
            request,
            "Account/Login/Index",
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
        return InertiaResponse(self.request, "Account/Login/Index", props={"valid": False})

    def form_valid(self, form):
        return super().form_valid(form)
