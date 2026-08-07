from allauth.account.views import LoginView
from inertia import inertia, InertiaResponse


class FundingLoginView(LoginView):
    def get(self, request):
        return InertiaResponse(
            request,
            "Account/Login/Index",
            props={
                "class_view": True,
            }
        )

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form, **kwargs):
        print("IIIIIIIIIII")
        return InertiaResponse(
            self.request,
            "Account/Login/Index",
            props={"valid": False}
        )


    def form_valid(self, form):
        print("VVVVVVVVV")
        return {"valid": True}
    