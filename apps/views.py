import urllib

import requests
from django.shortcuts import render, redirect
from django.views import View

from root import settings















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