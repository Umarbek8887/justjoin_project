from django.urls import path, re_path

from apps.views import RegisterCreateView, LoginFormView, ForgotPassword, SoicialLoginView, MainPage, \
    ActivateAccountView, CustomLogoutView

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('auth/register', RegisterCreateView.as_view(), name='register_page'),
    path('auth/login', SoicialLoginView.as_view(), name='login_page'),
    path('auth/login/by-email', LoginFormView.as_view(), name='login_by_email_page'),
    path('auth/password-reset', ForgotPassword.as_view(), name='password_reset_page'),
    path('auth/logout', CustomLogoutView.as_view(), name='logout_page'),
    re_path(r'^auth/user/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$',
            ActivateAccountView.as_view(), name='confirm_email_page'),
]