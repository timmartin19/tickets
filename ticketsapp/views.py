__author__ = 'Tim Martin'
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.shortcuts import render, redirect, render_to_response
from rest_framework import viewsets, permissions
from ticketsapp.models import Ticket
from ticketsapp.permissions import IsSuperuserOwnerOrReadOnly, TicketPermission
from ticketsapp.serializers import UserSerializer, TicketSerializer


def landing_view(request):
    return render_to_response('index.html')


@login_required()
def index_view(request):
    return render(request, 'base/base.html', dict(current_user=request.user.id))


def login_view(request):
    next_url = request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    if request.user is not None and request.user.is_authenticated():
        return redirect(next_url)
    if not request.POST:
        return render(request, 'base/login.html')
    user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
    if request.POST and user is not None and user.is_active:
        login(request, user)
        if not request.POST.get('remember_me'):
            request.session.set_expiry(0)
        return redirect(next_url)
    else:
        return render_to_response('base/login.html', {'invalid_login': True})


def logout_view(request):
    if request.user is not None and request.user.is_authenticated():
        logout(request)
    return redirect('login-view')


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (permissions.IsAuthenticated, TicketPermission,)

    def get_queryset(self):
        q = Ticket.objects.all()
        if not self.request.user.is_superuser:
            q = q.filter(Q(client=self.request.user) | Q(consultant=self.request.user))
        return q


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, IsSuperuserOwnerOrReadOnly,)

    def get_queryset(self):
        q = User.objects.all()
        filter_staff = self.request.QUERY_PARAMS.get('is_staff', None)
        if self.request.user.is_staff is False:
            q = q.filter(is_staff=True)
        elif filter_staff is not None:
            if filter_staff == 'true':
                is_staff = True
            else:
                is_staff = False
            q = q.filter(is_staff=is_staff)

        return q
