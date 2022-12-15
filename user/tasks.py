from celery import shared_task
from django.core.mail import send_mail as django_send_mail


@shared_task
def send_mail(subject, text, email):
    django_send_mail(subject, text, email, ['admin@example.com'])


@shared_task
def send_mail_with_comments(subject, text, email_sender, email_receiver):
    django_send_mail(subject, text, email_sender, [email_receiver])
