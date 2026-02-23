from django.urls import path

from apps.views import RegisterCreateView, LoginFormView, ForgotPassword, SoicialLoginView, PasswordSentView

urlpatterns = [
    path('auth/register', RegisterCreateView.as_view(), name='register_page'),
    path('auth/login', SoicialLoginView.as_view(), name='login_page'),
    path('auth/login/by-email', LoginFormView.as_view(), name='login_by_email_page'),
    path('auth/password-reset', ForgotPassword.as_view(), name='password_reset_page'),
    path('auth/password-sent', PasswordSentView.as_view(), name='password_sent_page'),
]