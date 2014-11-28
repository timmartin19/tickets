__author__ = 'Tim Martin'
from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from ticketsapp.models import Ticket


class TicketSerializer(ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('client', 'consultant', 'title', 'description', 'due_date',
                  'id', 'date_submitted', 'last_updated', 'status', 'progress_report',
                  'finished')


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'is_superuser', 'is_staff')