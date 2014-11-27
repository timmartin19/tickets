from django.shortcuts import render
from rest_framework import generics
from ticketsapp.models import Ticket
from ticketsapp.serializers import UserSerializer, TicketSerializer


class TicketBase(object):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class TicketDetail(generics.RetrieveUpdateAPIView, TicketBase):
    pass


class TicketList(generics.ListCreateAPIView, TicketBase):
    pass