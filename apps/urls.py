from django.urls import path, re_path

from apps.views import RegisterCreateView, LoginFormView, ForgotPassword, SoicialLoginView, MainPage, \
    ActivateAccountView, CustomLogoutView, JobDetailView, EmployerLoginView, EmployerRegisterView, \
    EmployerForgotPassword, GoogleLoginView, GoogleCallbackView, GithubLoginView, GithubCallbackView, \
    CandidateProfileView, SomethingView

# CandidateProfileUpdateView, CandidateProfileChangePasswordView, CandidateProfileInfoUpdateView, \
    # CandidateProfileImageUpdateView

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('job-offers/detail/<slug:slug>', JobDetailView.as_view(), name='detail'),
    path('test', SomethingView.as_view(), name='test'),


    path('profile', CandidateProfileView.as_view(), name="candidate_profile"),

    path('auth/register', RegisterCreateView.as_view(), name='register_page'),
    path('auth/login', SoicialLoginView.as_view(), name='login_page'),
    path('auth/login/by-email', LoginFormView.as_view(), name='login_by_email_page'),
    path('auth/password-reset', ForgotPassword.as_view(), name='password_reset_page'),
    path('auth/employer/login', EmployerLoginView.as_view(), name='employer_login_page'),
    path('auth/employer/register', EmployerRegisterView.as_view(), name='employer_register_page'),
    path('auth/employer/password-reset', EmployerForgotPassword.as_view(), name='employer_password_reset_page'),
    path('auth/logout', CustomLogoutView.as_view(), name='logout_page'),

    path('auth/google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('auth/google/callback/', GoogleCallbackView.as_view()),

    path('auth/github-login/', GithubLoginView.as_view(), name='github-login'),
    path('auth/github/callback/', GithubCallbackView.as_view()),



    re_path(r'^auth/user/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
            ActivateAccountView.as_view(), name='confirm_email_page'),
]