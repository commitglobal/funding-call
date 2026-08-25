import json

from allauth.account.views import LoginView
from inertia import InertiaResponse


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

    def form_invalid(self, form, **kwargs):
        return InertiaResponse(self.request, "Account/Login/Index", props={"valid": False})

    def form_valid(self, form):
        return super().form_valid(form)
