import random
from django.core.mail import EmailMessage, send_mail
from .models import User,OneTimePassword
from django.conf import settings
from django.shortcuts import get_object_or_404

def generate_otp():
    otp = ""
    for i in range(6):
        otp += str(random.randint(1,9))
    return otp

def send_code_to_user(email):
    subject = "One time passcode for Email verification"
    otp_code = generate_otp()
    print(otp_code,email)
    # user = User.objects.get(email=email)
    user = get_object_or_404(User, email=email)
    current_site = "MyAuth.com"
    email_body = (
        f"Hi {user.first_name},\n\n"
        f"Thanks for signing up on {current_site}.\n"
        f"Please verify your email using this one-time passcode:\n\n"
        f"🔐 {otp_code} 🔐\n\n"
        f"Regards,\n{current_site} Team"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    OneTimePassword.objects.create(user=user,code=otp_code)

    d_email = EmailMessage(subject=subject,body=email_body,from_email=from_email,to=[email])
    d_email.send(fail_silently=False)

def send_normal_email(data):
    email = EmailMessage(
        subject = data['email_subject'],
        body = data['email_body'],
        from_email = settings.DEFAULT_FROM_EMAIL,
        to = [data['to_email']]
    )
    email.send()