__author__ = 'Tim Martin'
from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from ticketsapp.models import Ticket
from ticketsapp.serializers import UserSerializer, TicketSerializer


def index_view(request):
    return render(request, 'base/base.html')


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer