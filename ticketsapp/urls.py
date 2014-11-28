__author__ = 'Tim Martin'
from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework_nested import routers
from ticketsapp.views import TicketViewSet, UserViewSet


router = routers.SimpleRouter()
router.register(r'ticket', TicketViewSet)
router.register(r'user', UserViewSet)

urlpatterns = patterns(
    '',
    url(r'^$', 'ticketsapp.views.index_view'),
    url(r'^api/', include(router.urls)),
)