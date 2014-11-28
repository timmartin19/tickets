from django.db import models
from django.contrib.auth.models import User


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
    finished = models.BooleanField(default=False)