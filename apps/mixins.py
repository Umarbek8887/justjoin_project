from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class LoginNotRequiredMixin:
    redirect_authenticated_user = True

    def get_success_url(self):
        if hasattr(self, 'success_url') and self.success_url:
            return str(self.success_url)
        return str(getattr(settings, 'LOGIN_REDIRECT_URL', reverse_lazy('main_page')))

    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)