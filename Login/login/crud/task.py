import string
from django.core.mail import send_mail,EmailMultiAlternatives
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordResetForm
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.core.mail import EmailMessage, get_connection
from django.utils.six import string_types

from celery import app

# Make sure our AppConf is loaded properly.
import djcelery_email.conf  # noqa
from djcelery_email.utils import dict_to_email, email_to_dict
from django.template import loader
from .models import user_token
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task

@shared_task
def create_random_user_accounts(email):
        send_mail(
            'celery',
            'Hi this mail has been send using celery.Soon you will be getting password reset mail with celery too.',
            'smartboyvicky05@gmail.com',
            [email],
            fail_silently=False,

        )



def sent_mail( email_template_name='registration/password_reset_email.html',subject_template_name='registration/password_reset_subject.txt'):
    subject = loader.render_to_string(subject_template_name)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template_name)
    send_mail(subject,body,'smartboyvicky05@gmail.com','vivek.vikash2014@codeflowtech.com',fail_silently=False)













