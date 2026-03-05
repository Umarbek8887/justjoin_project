from celery import shared_task



from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from apps.tokens import account_activation_token
from root.settings import EMAIL_HOST_USER

def send_email(subject: str, body: str | None, emails: list[str], html_content=None):
    email = EmailMultiAlternatives(subject=subject, body=body, from_email=EMAIL_HOST_USER, to=emails)
    email.attach_alternative(html_content, "text/html")
    try:
        email.send()
    except Exception as e:
        print(e)

@shared_task
def send_registration_link(user, host: str):
    subject = 'Successful Registration'
    token = account_activation_token.make_token(user)
    uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
    url = reverse_lazy('confirm_email_page', kwargs={'uidb64': uidb64, 'token': token})
    context = {
        'email': user.email,
        'confirm_link': host + url
    }
    html_content = render_to_string('justjoin/auth/candidate/registration-email.html', context)

    send_email(subject, None, [user.email], html_content)
