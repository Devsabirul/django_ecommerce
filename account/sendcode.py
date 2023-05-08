from django.conf import settings
from django.core.mail import send_mail


def sendOtp(name, code, email):
    subject = 'Verification Code'
    message = f'Hi {name},\nWe just need to verify your email address before you can access.\n\n\nVerify your email address with this {code} code.\n\n\n\nThanks!'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    print('send succefully')
    return message
