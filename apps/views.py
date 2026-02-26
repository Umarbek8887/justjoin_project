import urllib

import requests
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, TemplateView

from apps.forms import LoginForm, RegisterModelForm
from apps.mixins import LoginNotRequiredMixin
from root import settings



class LoginFormView(LoginNotRequiredMixin, FormView):
    template_name = 'justjoin/auth/login-by-email.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    # success_url = reverse_lazy('job_offer_list_page')

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)



class RegisterCreateView(LoginNotRequiredMixin, CreateView):
    template_name = 'justjoin/auth/register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('login_by_email_page')
    form_class = RegisterModelForm

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True  # Assuming we want them to login directly or just have them active. If not, they can't login.
        user.role = form.Meta.model.Roles.CANDIDATE  # Set default role
        user.save()
        return super().form_valid(form)



# Test
class ForgotPassword(TemplateView):
    template_name = 'justjoin/auth/password-reset.html'

# Test
class SoicialLoginView(TemplateView):
    template_name = 'justjoin/auth/login.html'


























# class GoogleLoginView(View):
#     def get(self, request):
#         scope = "email profile"
#         auth_url = (
#             f"https://accounts.google.com/o/oauth2/auth?response_type=code"
#             f"&client_id={settings.GOOGLE_CLIENT_ID}"
#             f"&redirect_uri={urllib.parse.quote(settings.GOOGLE_REDIRECT_URI)}"
#             f"&scope={urllib.parse.quote(scope)}"
#         )
#         return redirect(auth_url)
#
#
# class GoogleCallbackView(View):
#     def get(self, request):
#         code = request.GET.get("code")
#
#         token_data = {
#             "code": code,
#             "client_id": settings.GOOGLE_CLIENT_ID,
#             "client_secret": settings.GOOGLE_CLIENT_SECRET,
#             "redirect_uri": settings.GOOGLE_REDIRECT_URI,
#             "grant_type": "authorization_code",
#         }
#
#         token_res = requests.post("https://oauth2.googleapis.com/token", data=token_data).json()
#         access_token = token_res.get("access_token")
#
#         response = requests.get(
#             "https://www.googleapis.com/oauth2/v1/userinfo",
#             headers={"Authorization": f"Bearer {access_token}"}
#         )
#
#         if response.status_code == 200:
#             info = response.json()
#             email = info["email"]
#             name = info["name"]
#
#             user, created = User.objects.get_or_create(
#                 email=email,
#                 defaults={"first_name": name, 'is_active': True}
#             )
#             if not user.is_valid_password or created:
#                 user.set_unusable_password()
#                 user.save(update_fields=['password'])
#             login(request, user)
#
#             return redirect('product_list_page')
#         return redirect('login_page')