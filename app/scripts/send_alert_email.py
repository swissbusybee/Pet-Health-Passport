from app.models import Immunization
from datetime import datetime
from datetime import date
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User

def run():
    for immunization in Immunization.objects.all():
        if immunization.vaccine_expired:
            send_mail('Alert from Health Passport', 'Hello, One or more vaccines has expired, please login to your Health Passport profile to view the details.', settings.EMAIL_HOST_USER, [immunization.owner.email], fail_silently=True)