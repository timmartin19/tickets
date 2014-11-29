__author__ = 'Tim Martin'
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework_nested import routers
from ticketsapp.views import TicketViewSet, UserViewSet


router = routers.SimpleRouter(trailing_slash=False)
router.register(r'ticket', TicketViewSet)
router.register(r'user', UserViewSet)

urlpatterns = patterns(
    '',
    url(r'^/?$', 'ticketsapp.views.landing_view'),
    url(r'^management/$', 'ticketsapp.views.index_view', name="home"),
    url(r'^api/', include(router.urls)),
    url(r'^login/?$', 'ticketsapp.views.login_view', name='login-view'),
    url(r'^logout/?$', 'ticketsapp.views.logout_view', name='logout-view'),
)