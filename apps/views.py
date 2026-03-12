import secrets
import urllib.parse
import urllib.parse

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView, CreateView, TemplateView, ListView, DetailView, UpdateView

from apps.filters import JobOfferFilter
from apps.forms import LoginForm, RegisterModelForm, EmployerRegisterForm, EmployerLoginForm
from apps.mixins import LoginNotRequiredMixin
from apps.models import User, JobOffer, Category, CandidateUser
from apps.models.users import Roles
from apps.tasks import send_registration_link
from apps.tokens import account_activation_token
from root import settings


# class JobDetailView(DetailView):
#     queryset = JobOffer.objects.filter(is_active=True)
#     template_name = 'justjoin/main/job-detail.html'
#     context_object_name = 'job'
#
#     # def get_context_data(self, **kwargs):
#     #     context = super().get_context_data(**kwargs)
#     #     context["similar_jobs"] = JobOffer.objects.filter(category=)
#     #     return context


class JobDetailView(DetailView):
    queryset = (
        JobOffer.objects
        .filter(is_active=True)
        .select_related("company", "category")
        .prefetch_related("salaries")
    )
    template_name = "justjoin/main/job-detail.html"
    context_object_name = "job"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job = self.object
        similar_jobs = (
            JobOffer.objects
            .filter(is_active=True,
                    category=job.category,
                    company__origin=job.company.origin,
                    required_experience=job.required_experience
                    )
            .exclude(pk=job.pk)
            .select_related("company")
            .prefetch_related("salaries")
            .order_by("-published_at")[:4]
            .defer("description", "end_time", "created_at", "updated_at")
        )
        context["similar_jobs"] = similar_jobs
        return context


class MainPage(ListView):
    template_name = "justjoin/main/job-offers.html"
    context_object_name = "jobs"

    def get_queryset(self):
        qs = JobOffer.objects.filter(is_active=True).defer("description", "end_time", "created_at", "updated_at")
        qs = JobOfferFilter(self.request, qs).filter()
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["active_category"] = self.request.GET.get("category", "")
        context["active_working_mode"] = self.request.GET.getlist("working_mode")
        context["active_contract_type"] = self.request.GET.getlist("contract_type")
        context["active_working_type"] = self.request.GET.getlist("working_type")
        context["active_experience"] = self.request.GET.getlist("experience")
        context["salary_only"] = self.request.GET.get("salary_only", "")
        return context


class CandidateProfileView(LoginRequiredMixin, UpdateView):
    template_name = "justjoin/auth/candidate/profile.html"
    success_url = reverse_lazy("candidate_profile")

    def get(self, request, **kwargs):
        return render(request, self.template_name)

    def post(self, request, **kwargs):
        user = request.user
        profile = user.candidate_profile

        user.first_name = request.POST.get("first_name", "")
        user.last_name = request.POST.get("last_name", "")
        user.save()

        profile.message_to_employee = request.POST.get("message_to_employee", "")
        profile.linkedin_link = request.POST.get("linkedin_link", "")
        profile.github_link = request.POST.get("github_link", "")
        profile.other_link = request.POST.get("other_link", "")

        if request.FILES.get("image"):
            profile.image = request.FILES.get("image")

        if request.FILES.get("cv_file"):
            profile.cv_file = request.FILES.get("cv_file")

        profile.save()

        # messages.success(request, "Profile updated successfully.")
        return redirect(self.success_url)


class CandidateProfileChangePasswordView(LoginRequiredMixin, UpdateView):
    queryset = User.objects.all()
    template_name = 'justjoin/auth/candidate/profile.html'
    form_class = AdminPasswordChangeForm
    success_url = reverse_lazy('profile_page')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        kwargs.pop('instance')
        return kwargs

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        form.save()
        update_session_auth_hash(self.request, self.request.user)
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return super().form_invalid(form)


# Auth
class EmployerLoginView(LoginNotRequiredMixin, FormView):
    template_name = 'justjoin/auth/employer/login.html'
    form_class = EmployerLoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class EmployerRegisterView(LoginNotRequiredMixin, FormView):
    template_name = 'justjoin/auth/employer/register.html'
    form_class = EmployerRegisterForm
    redirect_authenticated_user = True

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save(update_fields=['is_active'])
        send_registration_link(user, f"{self.request.scheme}://{self.request.get_host()}")
        return self.render_to_response(self.get_context_data(form=form, success=True))


class LoginFormView(LoginNotRequiredMixin, FormView):
    template_name = 'justjoin/auth/candidate/login-by-email.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        login(self.request, form.user)
        return super().form_valid(form)


class RegisterCreateView(LoginNotRequiredMixin, CreateView):
    template_name = 'justjoin/auth/candidate/register.html'
    redirect_authenticated_user = True
    form_class = RegisterModelForm
    success_url = reverse_lazy('main_page')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.role = Roles.CANDIDATE
        user.save()
        send_registration_link(user, f"{self.request.scheme}://{self.request.get_host()}")
        return self.render_to_response(self.get_context_data(form=form, success=True))


class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        uid = None
        try:
            uid = force_bytes(urlsafe_base64_decode(uidb64)).decode()
            user = User.objects.get()
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save(update_fields=["is_active"])
            login(request, user)
            if user.role == 'candidate':
                CandidateUser.objects.create(user_id=uid)
            messages.success(request, "Email tasdiqlandi, endi bemalol login qilsa bo'ladi")
        else:
            messages.error(request, "Bu linkda xatolik bor")
        return redirect('main_page')


class CustomLogoutView(View):
    def get(self, request):
        next_page = request.GET.get('next') or request.META.get('HTTP_REFERER') or 'main_page'
        logout(request)
        # return redirect(next_page if next_page != 'candidate_profile' else '')
        return redirect(next_page)


# Test
class ForgotPassword(TemplateView):
    template_name = 'justjoin/auth/candidate/password-reset.html'


# Test
class EmployerForgotPassword(TemplateView):
    template_name = 'justjoin/auth/employer/reset-password.html'


class SoicialLoginView(LoginNotRequiredMixin, TemplateView):
    template_name = 'justjoin/auth/candidate/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('main_page')


# Google
class GoogleLoginView(View):
    def get(self, request):
        # CSRF hujumidan himoyalanish uchun state yaratamiz
        state = secrets.token_urlsafe(16)
        request.session['google_oauth2_state'] = state

        scope = "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"

        params = {
            "response_type": "code",
            "client_id": settings.GOOGLE_CLIENT_ID,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "scope": scope,
            "state": state,  # State qo'shildi
            "prompt": "select_account"  # Foydalanuvchiga akkauntni tanlash imkonini beradi
        }

        auth_url = f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"
        return redirect(auth_url)


class GoogleCallbackView(View):
    def get(self, request):
        state = request.GET.get("state")
        session_state = request.session.pop('google_oauth2_state', None)

        if not state or state != session_state:
            return redirect('login_page')  # State mos kelmasa, xavfli so'rov bo'lishi mumkin

        code = request.GET.get("code")
        if not code:
            return redirect('login_page')

        token_data = {
            "code": code,
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        }

        token_res = requests.post("https://oauth2.googleapis.com/token", data=token_data)
        if token_res.status_code != 200:
            return redirect('login_page')

        access_token = token_res.json().get("access_token")

        user_info_res = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {access_token}"}
        )

        if user_info_res.status_code == 200:
            info = user_info_res.json()
            email = info.get("email")
            first_name = info.get("given_name")
            last_name = info.get("family_name")
            picture_url = info.get("picture")

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first_name,
                    "last_name": last_name,
                    "is_active": True,
                    "role": Roles.CANDIDATE
                }
            )
            if created:
                CandidateUser.objects.create(user=user, image=picture_url)
                user.set_unusable_password()
                user.save()
            login(request, user)
            return redirect('main_page')

        return redirect('login_page')


# Github
class GithubLoginView(View):
    def get(self, request):
        state = secrets.token_urlsafe(16)
        request.session['github_oauth_state'] = state

        params = {
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": settings.GITHUB_REDIRECT_URI,
            "scope": "user:email",  # Foydalanuvchi emailini olish uchun ruxsat
            "state": state
        }
        auth_url = f"https://github.com/login/oauth/authorize?{urllib.parse.urlencode(params)}"
        return redirect(auth_url)


class GithubCallbackView(View):
    def get(self, request):
        state = request.GET.get("state")
        session_state = request.session.pop('github_oauth_state', None)

        if not state or state != session_state:
            return redirect('login_page')

        code = request.GET.get("code")
        if not code:
            return redirect('login_page')

        # 1. Access Token olish
        token_res = requests.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.GITHUB_CLIENT_ID,
                "client_secret": settings.GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": settings.GITHUB_REDIRECT_URI,
            },
            headers={"Accept": "application/json"}
        ).json()

        access_token = token_res.get("access_token")
        if not access_token:
            return redirect('login_page')

        headers = {"Authorization": f"token {access_token}"}
        user_res = requests.get("https://api.github.com/user", headers=headers).json()

        email = user_res.get("email")
        if not email:
            emails_res = requests.get("https://api.github.com/user/emails", headers=headers).json()
            email = next((e['email'] for e in emails_res if e['primary'] and e['verified']), emails_res[0]['email'])

        full_name = user_res.get("name") or user_res.get("login")
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "first_name": full_name,
                "role": Roles.CANDIDATE,
                "is_active": True
            }
        )

        if created:
            CandidateUser.objects.create(
                user=user,
                image=user_res.get("avatar_url"),
                github_link=user_res.get("html_url")
            )
            user.set_unusable_password()
            user.save()

        login(request, user)
        return redirect('main_page')
