from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.template import loader
import random
import string


class Ticket(models.Model):
    client = models.ForeignKey(User, related_name='client_tickets')
    consultant = models.ForeignKey(User, related_name='consultant_tickets')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField()
    date_submitted = models.DateTimeField(auto_now_add=True, auto_created=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=12, blank=True, null=True)
    progress_report = models.TextField(blank=True, null=True)


def send_new_password(sender, instance, created=False, **kwargs):
    if created and not settings.DEBUG:
        password = ''.join(random.choice(string.letters + string.digits) for _ in range(0, 15))
        instance.set_password(password)
        instance.save()
        context = {
            'user': instance,
            'username': instance.username,
            'password': password
        }
        body = loader.render_to_string('password_reset/new_user_email.txt',
                                       context).strip()
        subject = loader.render_to_string('password_reset/new_user_email_subject.txt',
                                          context).strip()
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                  [instance.email])

post_save.connect(send_new_password, sender=User)